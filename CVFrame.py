# A computer vision frame. Contains information about the kind of image it is when stored.

import CVEnumerations
import imutils


class CVFrame:
    def __init__(self, img, operation):
        if img is None:
            return None

        self.image = img
        self.width = len(img)
        self.height = len(img[0])
        self.operation = operation

    def get_image(self):
        return self.image

    # Replaces the current CVFrame with the incoming image.
    def replace_img(self, img):
        if img is None:
            return
        self.image = img
        self.width = len(img)
        self.height = len(img[0])

    def resize(self, width, height):
        res_img = self.image
        imutils.resize(res_img, width=width, height=height)

    def resize(self, scale=1):
        res_img = self.image
        imutils.resize(res_img, width=self.width * scale, height=self.height * scale)

        self.width = len(res_img)
        self.height = len(res_img[0])
        self.image = res_img
