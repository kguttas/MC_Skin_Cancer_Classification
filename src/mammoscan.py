import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image
from matplotlib.patches import Circle


class MammoScan:
    def __init__(self, scan, sc_info):
        self.__scan = scan
        self.__sc_info = sc_info

    @property  # scan image
    def scan(self):
        return self.__scan

    @property  # scan info
    def scan_info(self):
        return self.__sc_info

    @property  # from the scan file name
    def scan_name(self):
        return self.__sc_info.name

    @property  # x coordinate of the abnormality
    def x(self):
        return self.__sc_info.x

    @property  # y coordinate of the abnormality
    def y(self):
        return self.__sc_info.y

    @property  # radius of the abnormality
    def radius(self):
        return self.__sc_info.radius

    @property  # class of the abnormality
    def ab_class(self):
        return self.__sc_info.ab_class

    @property  # background tissue of the abnormality
    def bg(self):
        return self.__sc_info.bg

    @property  # severity of the abnormality
    def severity(self):
        return self.__sc_info.severity

    @property
    # generates cropped downsized rotated images of the abnormality
    def transformations(self):
        return self.__transform()

    @property
    # returns the matricial representation fo the scan image
    def pixel_matrix(self):
        return np.array(self.scan)

    # instance method
    def plot(self):

        # Create a figure. Equal aspect so circles look circular
        fig, ax = plt.subplots(1)

        fig.set_size_inches(8, 6)
        ax.set_aspect('equal')

        # Show the image
        ax.imshow(self.scan, cmap=plt.cm.gray_r)
        ax.set_ylim(bottom=0, top=1024)
        ax.set_title(self.scan_name)

        # create a circle to patch on the image
        x, y, r = self.__get_crop_coords()
        print(f'{x}, {y}, {r}')
        circ = Circle((x, y), r, fill=False)
        ax.add_patch(circ)

    # private method
    def __set_x(self, xValue):
        self.__sc_info.x = xValue

    # private method
    def __set_y(self, yValue):
        self.__sc_info.y = yValue

    # private method
    def __set_radius(self, rValue):
        self.__sc_info.radius = rValue

    # private method
    def __get_crop_coords(self):
        '''Returns a tuple with x, y and r'''
        # check scan class to decide on how to crop
        if pd.isnull(self.radius):
            radius = 48.0
            self.__set_radius(radius)
        if pd.isnull(self.x):
            x = float(np.random.randint(500, 513))
            self.__set_x(x)
        if pd.isnull(self.y):
            y = float(np.random.randint(500, 513))
            self.__set_y(y)

        return (self.x, 1024.0 - self.y, self.radius)

    # private method
    def __transform(self):
        '''Creates a dict
                  with rotated and mirrored versions of self.scan'''
        # create dictionary
        transformations = dict()
        # get crop values
        x, y, r = self.__get_crop_coords()
        # crop and resize scan
        cropped_scan = self.scan.crop((x - r, y - r, x + r, y + r))
        resized_scan = cropped_scan.resize((48, 48))
        # create rotated images
        for angle in (0, 90, 180, 270):
            rotated = resized_scan.rotate(angle)  # rotated by angle
            mirr_tp = rotated.transpose(Image.FLIP_TOP_BOTTOM)
            mirr_lr = rotated.transpose(Image.FLIP_LEFT_RIGHT)

            transformations[angle] = dict(zip(['rotated', 'mirr_lr', 'mirr_tp'],
                                              [rotated, mirr_lr, mirr_tp]))

        return transformations