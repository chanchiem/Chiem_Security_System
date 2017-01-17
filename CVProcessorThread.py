# Worker thread that processes images for vision operations. Reads images from CVCam.get_raw_image()
import threading
import CVEnumerations
import CVCam
import imutils
import cv2
import time
import numpy as np


class CVProcessorThread(threading.Thread):
    def __init__(self, __operation, __frame_manger):
        threading.Thread.__init__(self)
        self.operation = __operation
        self.isRunning = False
        self.frameManager = __frame_manger  # Main unit to write and read CVFrames

        self.face_cascade = cv2.CascadeClassifier(
            '/Users/ChiemSaeteurn/PycharmProjects/Cos429_Final/haarcascade_frontalface_default.xml')
        self.compFrame = None
        self.has_motion_detected = False
        self.start_time = time.time()

    def run(self):
        while self.isRunning:
            # RAW IMAGE OUTPUT
            if self.operation == CVEnumerations.RAW_IMAGE:
                grabbed, img = CVCam.get_raw_image()

                self.frameManager.create_frame(img, CVEnumerations.RAW_IMAGE)
            # FACE DETECTION
            elif self.operation == CVEnumerations.FACE_DETECTION:
                grabbed, img = CVCam.get_raw_image()
                height = len(img)
                width = len(img[0])
                face_detect_scale = 1  # resizing factor before we apply HAAR Cascade
                # This is the one used for face detection. Full resolution is not necessary.
                img_for_faces = imutils.resize(img, width=int(width * face_detect_scale),
                                               height=int(height * face_detect_scale))
                if not grabbed:
                    return

                gray = cv2.cvtColor(img_for_faces, cv2.COLOR_BGR2GRAY)
                faces = self.face_cascade.detectMultiScale(gray, 1.3, 5)
                for (x, y, w, h) in faces:
                    frame = cv2.rectangle(img, (int(x / face_detect_scale), int(y / face_detect_scale)), (
                        int(x / face_detect_scale + w / face_detect_scale),
                        int(y / face_detect_scale + h / face_detect_scale)),
                                          (255, 0, 0), 2)

                self.frameManager.create_frame(img, CVEnumerations.FACE_DETECTION)
            # MOTION DETECTION
            # This code was modified from code found on the follow website:
            # http://www.pyimagesearch.com/2015/05/25/basic-motion-detection-and-tracking-with-python-and-opencv/
            elif self.operation == CVEnumerations.MOTION_DETECTION:
                # global frameDeltaSumPrev
                # global frameDeltaSumCurr
                # global frameDelta
                grabbed, frame = CVCam.get_raw_image()

                if not grabbed:
                    break

                # Converts the image from rgb to gray and blurs the gray image
                gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                gray = cv2.GaussianBlur(gray, (21, 21), 0)

                # Sets the comparison frame to gray during the first run through this loop
                if self.compFrame is None:
                    self.compFrame = gray
                    continue

                # Resets the comparison frame every five seconds
                timeElapsed = time.time() - self.start_time
                if timeElapsed > 5:
                    self.start_time = time.time()
                    self.compFrame = gray

                    # Resets timeElapsed counter if camera detects movement
                    # if frameDelta is not None:
                    #   frameDeltaSumPrev = np.sum(np.sum(frameDelta))
                #	frameDeltaSumCurr = np.sum(np.sum(cv2.absdiff(firstFrame, gray)))
                #	if abs(int(frameDeltaSumPrev) - int(frameDeltaSumCurr)) > 20000:
                #		start = time.time()

                # Computes the absolute difference in pixel values of the comparison
                # frame and the current frame
                frameDelta = cv2.absdiff(self.compFrame, gray)
                thresh = cv2.threshold(frameDelta, 25, 255, cv2.THRESH_BINARY)[1]
                thresh = cv2.dilate(thresh, None, iterations=2)
                (_, cnts, _) = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL,
                                                cv2.CHAIN_APPROX_SIMPLE)

                # Draws rectangles around the areas where motion was detected
                if len(cnts) == 0:
                    self.has_motion_detected = False
                for c in cnts:
                    if cv2.contourArea(c) < 500:
                        continue
                    (x, y, w, h) = cv2.boundingRect(c)
                    cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
                    self.has_motion_detected = True

                self.frameManager.create_frame(frame, CVEnumerations.MOTION_DETECTION)
            # CANNY EDGE DETECTION
            elif self.operation == CVEnumerations.CANNY_EDGE_DETECTION:
                grabbed, img = CVCam.get_raw_image()
                img = cv2.Canny(img, 100, 200)

                self.frameManager.create_frame(img, CVEnumerations.CANNY_EDGE_DETECTION)
            # CORNER DETECTION
            elif self.operation == CVEnumerations.CORNER_DETECTION:
                grabbed, img = CVCam.get_raw_image()
                gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
                gray = np.float32(gray)
                dst = cv2.cornerHarris(gray, 2, 7, 0.04)

                # result is dilated for marking the corners, not important
                dst = cv2.dilate(dst, None)

                # Threshold for an optimal value, it may vary depending on the image.
                img[dst > 0.01 * dst.max()] = [0, 0, 255]

                self.frameManager.create_frame(img, CVEnumerations.CORNER_DETECTION)
            # KEYPOINT DETECTION
            elif self.operation == CVEnumerations.KEYPOINT_DETECTION:
                grabbed, img = CVCam.get_raw_image()

                if not grabbed:
                    break
                gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

                sift = cv2.xfeatures2d.SIFT_create()
                kp = sift.detect(gray, None)
                frame = cv2.drawKeypoints(gray, kp, img)

                self.frameManager.create_frame(img, CVEnumerations.KEYPOINT_DETECTION)

    def get_operation(self):
        return self.operation

    def set_operation(self, input_operation):
        self.operation = input_operation
