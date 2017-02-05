# Segmentation modes
OSD = 0                      # OSD only
AUTOMATIC_OSD = 1            # Automatic page segmentation with OSD
AUTOMATIC_NO_OSD = 2         # Automatic page segmentation, but no OSD, or OCR
DEFAULT = 3                  # Fully automatic page segmentation, but no OSD. (Default)
BLOCK_VERTICAL_VARIABLE = 4  # Assume a single column of text of variable sizes.
BLOCK_VERTICAL_UNIFORM = 5   # Assume a single uniform block of vertically aligned text.
BLOCK_SINGLE = 6             # Assume a single uniform block of text.
SINGLE_LINE = 7              # Treat the image as a single text line.
SINGLE_WORD = 8              # Treat the image as a single word.
SINGLE_WORD_CIRCLE = 9       # Treat the image as a single word in a circle.
SINGLE_CHARACTER = 10        # Treat the image as a single character.

# languages
ENGLISH = 'eng'

import subprocess


class Tesseract:
    def __init__(self, image):
        self.image = image

    def get_text(self, **kwargs) -> str:
        command = self._create_command(**kwargs)
        print(command)
        result = subprocess.Popen(command, shell=True,
                         universal_newlines=True, stdout=subprocess.PIPE,
                         stderr=subprocess.PIPE)
        return result.stdout.read()

    def _create_command(self, **options) -> str:
        language = options.get('lanugage', ENGLISH)
        seg = options.get('segment', DEFAULT)
        image = self.image

        # tesseract command line
        command = f'tesseract -l {language} -psm {seg} {image} stdout'

		return command
