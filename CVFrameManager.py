## Class used to handle computer vision frames.

from CVFrame import CVFrame
from collections import deque


class CVFrameManager:
    def __init__(self, buffer_size=64):
        self.frames = deque([], buffer_size)
        self.frameChangedSinceLastRead = False
        self.totalFramesAdded = 0

    # Creates a CVFrame object and stores it into the manager.
    def create_frame(self, img, operation, scale=1):
        frame = CVFrame(img, operation)
        frame.resize(scale)
        self.append_frame(frame)

    # Appends a passed in CVFrame object into the frame buffer.
    # This stores it into the top of the stack.
    def append_frame(self, frame):
        self.frames.append(frame)
        self.frameChangedSinceLastRead = True
        self.totalFramesAdded += 1

    # Changes the max amount of frames that the buffer can hold.
    # If the passed in size is less than the current max buffer length,
    # the buffer is concatenated accordingly, preserving the latest frames.
    def change_buffer_size(self, new_size):
        self.frames = deque(self.frames, new_size)

    # Returns the max length of the buffer. If the buffer exceeds this amount,
    # then it acts like a circular buffer.
    def get_max_buffer_length(self):
        return self.frames.maxlen

    # Returns the current buffer size.
    def get_buffer_size(self):
        return len(self.frames)

    # Reads the least recently added frame. It doesn't remove it from the buffer.
    def read_first_frame(self):
        if self.get_buffer_size() == 0:
            return None

        self.frameChangedSinceLastRead = False
        return self.frames[0]

    # Reads and removes the least recently added frame.
    def pop_first_frame(self):
        if self.get_buffer_size() == 0:
            return None

        return self.frames.popleft()

    # Reads the most recently added frame.
    def read_last_frame(self):
        if self.get_buffer_size() == 0:
            return None
        self.frameChangedSinceLastRead = False

        return self.frames[-1]

    # Reads and removes the most recently added frame.
    def pop_last_frame(self):
        if self.get_buffer_size() == 0:
            return None

        return self.frames.pop()

    def empty_frames(self):
        self.frames.clear()

    # Returns the total amount of frames that have been added so far
    # in this buffer.
    def total_frames_added(self):
        return self.totalFramesAdded

    # This is true if a frame has already been pushed since the last read occurred.
    def frame_changed_since_last_read(self):
        return self.frameChangedSinceLastRead
