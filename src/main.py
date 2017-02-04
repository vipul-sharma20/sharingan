import sys

import cv2

from tesseract import Tesseract


class Image:

    class THRESHOLD:
        MEAN = cv2.ADAPTIVE_THRESH_MEAN_C
        GAUSSIAN = cv2.ADAPTIVE_THRESH_GAUSSIAN_C
        IMG_PATH = 'image_processed.jpg'
        WINDOW = 'threshold'
        TRACK_BLOCK = 'block_size'
        TRACK_C = 'constant'
        RANGE = [3, 19]

        # OpenCV 3.2 doesn't allow parameters in callback so globals
        thresh_type = GAUSSIAN
        block_size = 3
        c = 2

    def __init__(self, image: str, *args, **kwargs):
        self.image = cv2.imread(image, 0)

    def threshold(self, thresh_type: int, block_size: int, c: int,
                  callback=False, **kwargs):
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
        img = cv2.medianBlur(self.image, 5)

        thresh_img = cv2.adaptiveThreshold(img, 255, thresh_type,
                                           cv2.THRESH_BINARY, block_size, c)

        # Temporary jugaad
        cv2.imwrite(Image.THRESHOLD.IMG_PATH, thresh_img)

        return thresh_img

    def transform(self, *args, **kwargs):
        raise NotImplementedError

    def crop(self, *args, **kwargs):
        raise NotImplementedError

    def get_text(self, *args, **kwargs) -> str:
        """
        Extract text from thresholded image

        :param: None
        :returns: text extracted
        """
        tess_obj = Tesseract(Image.THRESHOLD.IMG_PATH)
        text = tess_obj.get_text()

        return text

    def resize(self, resize_by: int, *args, **kwargs):
        """
        Resize large dimesion images

        :param img: Large dimension image to be resized
        :returns: resized image
        """
        new_x, new_y = self.image.shape[1] // resize_by, \
                       self.image.shape[0] // resize_by

        self.image = cv2.resize(self.image, (new_x, new_y))

    def show_thresh(self, thresh_img=None, *args, **kwargs):
        """
        Prepare image window and show image

        :param img: Default thresholded image
        :returns: None
        """
        c = Image.THRESHOLD
        cv2.namedWindow(c.WINDOW)
        cv2.createTrackbar(c.TRACK_BLOCK, c.WINDOW, c.RANGE[0], c.RANGE[1],
                           self._block_size_thresh)
        if thresh_img is None:
            thresh_img = self.image

        while True:
            cv2.imshow(c.WINDOW, thresh_img)
            k = cv2.waitKey(1) & 0xFF
            if k == 27:
                sys.exit(0)

    def _block_size_thresh(self, preset, *args, **kwargs):
        """
        Trackbar change callback

        :param preset: preset value from trackbar
        :returns: None
        """
        # get preset odd value
        block_size = preset*2 + 1
        t = Image.THRESHOLD

        thresh_image = self.threshold(thresh_type=t.thresh_type, callback=True,
                                      block_size=block_size, c=t.c)
        self.show_thresh(thresh_image)

