########################################################################
########################################################################
## This is the universal implementation of a singleton camera class.
## This  will allow clients to sample
## live images from the camera and live video feeds.
## One unique property of this class is that it maintains a circular
## buffer of video data with a size of about 15 seconds. This will allow
## users to acquire video feed 15 seconds before.
########################################################################
########################################################################
import cv2
import imutils
import CVEnumerations
import threading
import time
from CVFrameManager import CVFrameManager
from CVProcessorThread import CVProcessorThread

####################
# Global Variables #
####################
image_out_scale = None
cam = None
cv_thread = None
start = None
has_motion_detected = None
notify_on_motion_detect = None
frame_manager = None


########################


############################

def get_current_cv_operation():
    return cv_thread.get_operation()


def sample_image_from_operation():
    # global img
    frame = frame_manager.read_last_frame()
    img = frame.get_image()

    ret, jpg_img = cv2.imencode('.jpg', img)

    return jpg_img


def set_image_scale(scale):
    global image_out_scale
    image_out_scale = scale


def get_raw_image(scale=True):
    ret, raw_img = cam.read()
    if scale:
        height = len(raw_img)
        width = len(raw_img[0])
        res_img = imutils.resize(raw_img, width=int(width * image_out_scale), height=int(height * image_out_scale))
    else:
        res_img = raw_img
    return ret, res_img


# Returns the image after cv operations
def get_raw_cv_image():
    return frame_manager.read_last_frame()


def switch_cv_operation(operation=CVEnumerations.RAW_IMAGE):
    global cv_thread
    cv_thread.set_operation(operation)


def start_cv_operation():
    global cv_thread
    if cv_thread is not None:
        if not cv_thread.isRunning:
            cv_thread.isRunning = True
            cv_thread.start()


def has_motion_detect():
    return has_motion_detected


def set_notify_on_motion(state):
    global notify_on_motion_detect
    notify_on_motion_detect = state


def get_notify_on_motion():
    global notify_on_motion_detect
    return notify_on_motion_detect


def stop():
    cv_thread.isRunning = False
    cam.release()
    frame_manager.empty_frames()


def start_recording():
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    width = int(cam.get(cv2.CAP_PROP_FRAME_WIDTH) * image_out_scale)
    height = int(cam.get(cv2.CAP_PROP_FRAME_HEIGHT) * image_out_scale)
    fps = cam.get(cv2.CAP_PROP_FPS)
    out = cv2.VideoWriter('~/output.mp4', fourcc, fps, (width, height))
    import os
    cwd = os.getcwd()
    print cwd
    for i in range(1, 60):
        global img
        out.write(img)
        threading.Lock()


######################
## Start Everything ##
######################

set_image_scale(.5);

print "Starting up camera..."
cam = cv2.VideoCapture(1)
time.sleep(.5)

frame_manager = CVFrameManager()
frame_manager.create_frame(get_raw_image()[1], CVEnumerations.RAW_IMAGE)

cv_thread = CVProcessorThread(CVEnumerations.RAW_IMAGE, frame_manager)

start = time.time()
has_motion_detected = False
notify_on_motion_detect = False
# frameDeltaSumPrev = 0
# frameDeltaSumCurr = 0
# frameDelta = None
