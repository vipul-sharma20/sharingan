import random
import sys
import os
from glob import glob

import cv2
import numpy as np

from tesseract import Tesseract
from constants import WINDOW, POINT_COLOR, SEGMENTED_PLACEHOLDER


class Image:

    class THRESHOLD:
        MEAN = cv2.ADAPTIVE_THRESH_MEAN_C
        GAUSSIAN = cv2.ADAPTIVE_THRESH_GAUSSIAN_C
        IMG_PATH = 'thresholded/{name}'
        WINDOW = 'threshold'
        TRACK_BLOCK = 'block_size'
        TRACK_C = 'constant'
        BLOCK_SIZE_RANGE = [1, 9]
        C_RANGE = [1, 10]
        AUTO_BLOCK_SIZE = 17
        AUTO_C = 6

        # OpenCV 3.2 doesn't allow parameters in callback so globals
        thresh_type = GAUSSIAN
        block_size = 3
        c = 2

    def __init__(self, image: str, *args, **kwargs):
        self.original = cv2.imread(image)
        self.image = self.original.copy()  # never changes
        self.draw_image = self.original.copy()
        self.gray = cv2.cvtColor(self.original, cv2.COLOR_BGR2GRAY)
        self.path = []
        self.rectangle = False
        self.resize_factor = 1

    def threshold(self, thresh_type: int, block_size: int, c: int,
                  auto_thresh=False, **kwargs):
        """
        Threshold image

        :param thresh_type: mean/gaussian adaptive thresholding
        :param block_size: Size of a pixel neighborhood that is used to
                           calculate a threshold value for the pixel: 3, 5, 7,
                           and so on.
        :param c: constant subtracted from the mean or weighted mean
        :returns: thresholded image
        """
        self.thresh_type = thresh_type

        if auto_thresh:
            for i in glob('segmented/*.jpg'):
                img = cv2.imread(i, 0)
                self._threshold(img, thresh_type, block_size, c,
                                os.path.basename(i))
            return
        else:
            img = self.gray
            return self._threshold(img, thresh_type, block_size, c, 't.jpg')

    def transform(self, *args, **kwargs):
        raise NotImplementedError

    def resize(self, resize_by: int, *args, **kwargs):
        """
        Resize large dimesion images

        :param img: Large dimension image to be resized
        :param resize_by: times by which to resize
        :returns: resized image
        """
        new_x, new_y = self.original.shape[1] // resize_by, \
                       self.original.shape[0] // resize_by

        self.gray = cv2.resize(self.gray, (new_x, new_y))
        self.draw_image = cv2.resize(self.draw_image, (new_x, new_y))
        self.original = cv2.resize(self.draw_image, (new_x, new_y))
        self.resize_factor = resize_by

    def show_thresh(self, thresh_img=None, *args, **kwargs):
        """
        Prepare image window and show image

        :param img: Default thresholded image
        :returns: None
        """
        c = Image.THRESHOLD
        cv2.namedWindow(c.WINDOW)
        cv2.createTrackbar(c.TRACK_BLOCK, c.WINDOW, c.BLOCK_SIZE_RANGE[0],
                           c.BLOCK_SIZE_RANGE[1], self._callback_thresh)
        cv2.createTrackbar(c.TRACK_C, c.WINDOW, c.C_RANGE[0], c.C_RANGE[1],
                           self._callback_thresh)
        if thresh_img is None:
            thresh_img = self.gray

        while True:
            cv2.imshow(c.WINDOW, thresh_img)
            self._wait_key(1, c.WINDOW)

    def show_image(self, is_crop=True, *args, **kwargs):
        """
        Show original image image

        :param is_crop: handle mouse click or mouse drag (cropping)
        """
        cv2.namedWindow(WINDOW)

        if is_crop:
            cv2.setMouseCallback(WINDOW, self._mouse_crop_callback)

            while True:
                cv2.imshow(WINDOW, self.draw_image)
                self._wait_key(1, WINDOW)
        else:
            cv2.setMouseCallback(WINDOW, self._mouse_click_callback)
            while True:
                cv2.imshow(WINDOW, self.gray)
                self._wait_key(20, WINDOW)

    def auto_segment(self, *args, **kwargs):
        """
        Auto segmentation of text

        :returns: None
        """
        blur = cv2.GaussianBlur(self.draw_image, (9, 9), 0)
        edged = cv2.Canny(blur, 0, 100)
        dilated = cv2.dilate(edged, np.ones((15, 15)))

        _, contours, _ = cv2.findContours(dilated, cv2.RETR_EXTERNAL,
                                          cv2.CHAIN_APPROX_SIMPLE)
        for i, contour in enumerate(contours):
            if not self._contour_approx_bad(contour):
                rect = cv2.boundingRect(contour)
                x, y, w, h = [r*self.resize_factor for r in rect]
                b, g = random.sample(range(0, 255), 2)
                cv2.rectangle(self.image, (x,y), ((x+w), (y+h)), (b, g, 255), 10)
                self.crop(name=str(i), **{'start': (x,y),
                                          'end': ((x+w), (y+h))})

        return self.image

    def crop(self, name, is_poly=False, *args, **kwargs):
        """
        Crop image

        :param name: File name to save
        :param is_poly: True if polygon masked cropping
        :returns: None
        """
        if is_poly:
            self._crop_poly(name)
        else:
            self._crop_rect(name, **kwargs)

    def _contour_approx_bad(self, contour, *args, **kwargs):
        """
        Approximate contour and discard non rectangular contours

        :returns: True if rectangle else False
        """
        perimeter = cv2.arcLength(contour, True)
        approx = cv2.approxPolyDP(contour, 0.02*perimeter, True)

        return len(approx) == 4

    def _crop_rect(self, name, **kwargs):
        """
        Crop rectangular image

        :param start: top left coordinates
        :param end: bottom right coordinates
        :returns: None
        """
        x1, y1 = kwargs['start']
        x2, y2 = kwargs['end']
        crop_img = self.image[y1:y2, x1:x2]
        cv2.imwrite(SEGMENTED_PLACEHOLDER.format(name=name), crop_img)

    def _crop_poly(self, name, *args, **kwargs):
        """
        Crop by the coordinates of mouse clicks

        :returns: None
        """
        mask = np.zeros(self.gray.shape, dtype=np.uint8)
        roi_corners = np.array([self.path], dtype=np.int32)
        channel_count = 2
        ignore_mask_color = (255,) * channel_count
        cv2.fillPoly(mask, roi_corners, ignore_mask_color)

        masked_image = cv2.bitwise_and(self.gray, mask)

        cv2.imwrite(SEGMENTED_PLACEHOLDER.format(name=name), masked_image)

    def _threshold(self, img, thresh_type, block_size, c, name):
        img = cv2.medianBlur(img, 5)

        thresh_img = cv2.adaptiveThreshold(img, 255, thresh_type,
                                           cv2.THRESH_BINARY, block_size, c)
        # Temporary jugaad
        cv2.imwrite(Image.THRESHOLD.IMG_PATH.format(name=name), thresh_img)

        return thresh_img

    def _callback_thresh(self, preset: int, *args, **kwargs):
        """
        Trackbar change callback

        :param preset: preset value from trackbar
        :returns: None
        """

        t = Image.THRESHOLD

        # get preset odd value
        t.block_size = cv2.getTrackbarPos(t.TRACK_BLOCK, t.WINDOW)*2 + 1
        t.c = cv2.getTrackbarPos(t.TRACK_C, t.WINDOW)

        thresh_image = self.threshold(thresh_type=t.thresh_type,
                                      auto_thresh=False,
                                      block_size=t.block_size, c=t.c)
        self.show_thresh(thresh_image)

    def _mouse_click_callback(self, event: int, x: int, y: int, *args,
                              **kwargs):
        """
        Mouse event callback

        :param event: event integer value
        :param x: coordinate x value
        :param y: coordinate y value
        :returns: None
        """
        if event == cv2.EVENT_LBUTTONUP:
            self.path.append((x, y))
            cv2.circle(self.gray, (x, y), 4, POINT_COLOR, -1)

    def _mouse_crop_callback(self, event: int, x: int, y: int, *args, **kwargs):
        global start_x, start_y

        if event == cv2.EVENT_LBUTTONDOWN:
            self.path = []
            self.rectangle = True
            start_x = x
            start_y = y
            self.draw_image = self.original.copy()
            cv2.rectangle(self.draw_image, (x, y), (x, y), (0, 255, 0))

        elif event == cv2.EVENT_LBUTTONUP:
            self.rectangle = False
            self.draw_image = self.original.copy()
            self.path.extend([(start_x, start_y), (x, y)])
            cv2.rectangle(self.draw_image, (start_x, start_y), (x, y),
                          (0, 255, 0))

        elif event == cv2.EVENT_MOUSEMOVE:
            if self.rectangle:
                self.draw_image = self.original.copy()
                cv2.rectangle(self.draw_image, (start_x, start_y), (x, y),
                              (0, 255, 0))

    def _wait_key(self, k: int, window: str, type=None, *args, **kwargs):
        """
        Wrapper around cv2.waitKey

        :param k: delay in ms
        :param window: window name
        :param type: window type (TODO: WHY ?)
        :returns: None
        """
        k = cv2.waitKey(k) & 0xFF
        if k == 27:
            cv2.destroyAllWindows()
        elif k == 13:
            # Dayum!
            x1, y1, x2, y2 = [coord*self.resize_factor for sublist in self.path
                              for coord in sublist]
            self.crop(name='rect', **{'start': (x1, y1), 'end': (x2, y2)})

