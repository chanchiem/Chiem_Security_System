# Module that records CVFrames into specified outputs.
# This reads from the frame manager to record the video into the output.

import cv2
import TCEnumerations
import CVFrameManager
import CVFrame


class CVFrameRecorder:
    def __init__(self, __codec__=TCEnumerations.CV_FRAME_RECORDER_MP4V, __frameManager__):
        self.codec = __codec__
        self.frameManager = __frameManager__

    def start_recording(self):
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        width = int(cam.get(cv2.CAP_PROP_FRAME_WIDTH) * image_out_scale)
        height = int(cam.get(cv2.CAP_PROP_FRAME_HEIGHT) * image_out_scale)
        fps = cam.get(cv2.CAP_PROP_FPS)
        out = cv2.VideoWriter('~/output' + random.randint(1, 5000) + '.mp4', fourcc, fps, (width, height))
        import os
        cwd = os.getcwd()
        print cwd
        for i in range(1, 60):
            global img
            out.write(img)
            threading.Lock()
