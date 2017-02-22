from glob import glob

from main import Image
from tesseract import Tesseract


def main():
    i = Image('/Users/vipul/Downloads/IMG_20170212_181147_01.jpg')
    i.resize(4)
    i.auto_segment()
    i.threshold(thresh_type=Image.THRESHOLD.GAUSSIAN, block_size=17, c=6,
                auto_thresh=True)

    data = []
    percent = lambda n, d: (n/d)*100 if d else 0

    for img in glob('thresholded/*.jpg'):
        tess_obj = Tesseract(img)
        text = tess_obj.get_text()
        others = len(text) - \
            sum(c.isalpha() or c.isdigit() or c.isspace for c in text)
        per = percent(others/len(text))
        if len(text) > 5:
            data.append(text)
    return data
