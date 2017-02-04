import cv2

from tesseract import Tesseract


class Image:

    class THRESHOLD:
        MEAN = cv2.ADAPTIVE_THRESH_MEAN_C
        GAUSSIAN = cv2.ADAPTIVE_THRESH_GAUSSIAN_C
        IMG_PATH = 'image_processed.jpg'

    def __init__(self, image: str, *args, **kwargs):
        self.image = cv2.imread(image, 0)

    def threshold(self, thresh_type: int, block_size: int, c: int, **kwargs):
        """
        Threshold image

        :param thresh_type: mean/gaussian adaptive thresholding
        :param block_size: Size of a pixel neighborhood that is used to
                           calculate a threshold value for the pixel: 3, 5, 7,
                           and so on.
        :param c: constant subtracted from the mean or weighted mean
        :returns: thresholded image
        """
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
