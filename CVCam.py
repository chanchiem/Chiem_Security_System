########################################################################
########################################################################
## This is the universal implementation of a singleton camera class.
## This  will allow clients to sample
## live images from the camera and live video feeds.
## Use this for cross-platform camera usage.
########################################################################
########################################################################
import cv2
import imutils
import TCEnumerations
import threading
import time
import random
from CVFrameManager import CVFrameManager
from CVProcessorThread import CVProcessorThread


# ####################
# # Global Variables #
# ####################
# cam_type = None
# image_out_scale = 0.5
# cam = None
# cv_thread = None
# start = None
# has_motion_detected = None
# notify_on_motion_detect = None
# frame_manager = None
# has_loaded = False
#
# rawCapture = None  # Used for pi cams only


############################

class CVCam(object):
    def __init__(self):
        ##
        # FORWARD DECLARE ALL VARIABLES THAT WILL BE USED #
        ##
        # The device type; raspberry pi or regular computer
        self.cam_type = None
        # The output scale when we sample from this module.
        self.image_out_scale = 0.5
        # The camera object itself
        self.cam = None
        # The vision processing thread
        self.cv_thread = None
        self.start = None
        # Flag to check if motion has been detected
        self.has_motion_detected = None
        # Flag to notify clients if the motion has been detected
        self.notify_on_motion_detect = None
        # Object that stores the frames into a buffer.
        self.frame_manager = None
        self.has_loaded = False
        # Used for PI_Cams only
        self.rawCapture = None

        ##
        # START INITIALIZING THE CAMERA #
        ##
        print "Starting up camera..."
        self.init_camera()

    # Initializes the camera for use. Depends on specific flag set.
    def init_camera(self):
        # Check the device type
        try:
            from picamera import PiCamera
            from picamera.array import PiRGBArray
            self.cam_type = TCEnumerations.DEVICE_RASPBERRY
        except ImportError:
            self.cam_type = TCEnumerations.DEVICE_REGULAR_COMPUTER

        ##
        # Declare the actual camera object.
        ##
        if self.cam_type == TCEnumerations.DEVICE_RASPBERRY:
            self.cam = PiCamera()
            self.rawCapture = PiRGBArray(self.cam)
            print "Device Type Detected: Raspberry Pi"
        elif self.cam_type == TCEnumerations.DEVICE_REGULAR_COMPUTER:
            self.cam = cv2.VideoCapture(1)
            print "Device Type Detected: Regular Computer"
        else:
            self.cam = cv2.VideoCapture(1)
            print "No default camera flag set; defaulting to cv2..."

        ##
        # Initialize the frame manager
        ##
        time.sleep(.5)
        self.frame_manager = CVFrameManager()
        self.frame_manager.create_frame(self.get_raw_image()[1], TCEnumerations.CV_RAW_IMAGE)

        ##
        # Initialize the Vision Processing Thread and all its flags
        ##
        self.cv_thread = CVProcessorThread(self, TCEnumerations.CV_RAW_IMAGE, self.frame_manager)
        self.start = time.time()
        self.has_motion_detected = False
        self.notify_on_motion_detect = False

    # Gets the current Computer Vision Processing thread.
    def get_current_cv_operation(self):
        return self.cv_thread.get_operation()

    def sample_image_from_operation(self):
        frame = self.frame_manager.read_last_frame()
        img = frame.get_image()
        ret, jpg_img = cv2.imencode('.jpg', img)
        return jpg_img

    def set_image_scale(self, scale):
        self.image_out_scale = scale

    def get_raw_image(self, scale=True):
        # Sample image as from Pi Camera or regular CV Cam?
        if self.cam_type == TCEnumerations.DEVICE_RASPBERRY:
            self.rawCapture.truncate(0)
            self.cam.capture(self.rawCapture, format="bgr", use_video_port=True)
            raw_img = self.rawCapture.array
            ret = raw_img is not None
        else:
            ret, raw_img = self.cam.read()

        # Scale the image and then return it.
        if scale:
            height = len(raw_img)
            width = len(raw_img[0])
            res_img = imutils.resize(raw_img, width=int(width * self.image_out_scale),
                                     height=int(height * self.image_out_scale))
        else:
            res_img = raw_img

        return ret, res_img

    # Returns the image after cv operations
    def get_raw_cv_image(self):
        return self.frame_manager.read_last_frame()

    def switch_cv_operation(self, operation=TCEnumerations.CV_RAW_IMAGE):
        self.cv_thread.set_operation(operation)

    def start_cv_operation(self):
        if self.cv_thread is not None:
            if not self.cv_thread.isRunning:
                self.cv_thread.isRunning = True
                self.cv_thread.start()

    def has_motion_detect(self):
        return self.has_motion_detected

    def set_notify_on_motion(self, state):
        self.notify_on_motion_detect = state

    def get_notify_on_motion(self):
        return self.notify_on_motion_detect

    def stop(self):
        # cv_thread.stop_processing()
        self.cam.release()
        self.frame_manager.empty_frames()

    def start_recording(self):
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        width = int(self.cam.get(cv2.CAP_PROP_FRAME_WIDTH) * image_out_scale)
        height = int(self.cam.get(cv2.CAP_PROP_FRAME_HEIGHT) * image_out_scale)
        fps = self.cam.get(cv2.CAP_PROP_FPS)
        out = cv2.VideoWriter('~/output' + random.randint(1, 5000) + '.mp4', fourcc, fps, (width, height))
        import os
        cwd = os.getcwd()
        print cwd
        for i in range(1, 60):
            global img
            out.write(img)
            threading.Lock()

# # Returns the singleton object of camera
# def singleton_factory(_singleton=CVCam()):
#     return _singleton

######################
## Start Everything ##
######################

# This ensures that this module only initializes once.
# set_image_scale(.25) # This is actually handled by webserver
