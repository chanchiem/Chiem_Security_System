## Class used to handle computer vision frames.

import CVFrame
from collections import deque


class CVFrameManager:
    def __init__(self, buffer_size=1024):
        self.buffer_size = buffer_size  # Hold 1024 frames
        self.frames = deque([], buffer_size)

    def create_frame(self, img, operation):
        frame = CVFrame(img, operation)
        self.frames.append(frame)
