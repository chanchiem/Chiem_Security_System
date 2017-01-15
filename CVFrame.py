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

    def replace_img(self, img):
        if img is None:
            return
        self.image = img
        self.width = len(img)
        self.height = len(img[0])

    def resize(self, width, maintain_aspect_ratio=True, height=-1):
        res_img = self.img
        if maintain_aspect_ratio:
            imutils.resize(res_img, width=width)
        else:
            imutils.resize(res_img, width=width, height=height)