#########################
## GLOBAL ENUMERATIONS ##
#########################

###
# Device Flag Enumerations #
###
DEVICE_RASPBERRY = 0
DEVICE_REGULAR_COMPUTER = 1  # Generic Computer

###
# Computer Vision Operations ##
###
CV_RAW_IMAGE = 0
CV_FACE_DETECTION = 1
CV_MOTION_DETECTION = 2
CV_CANNY_EDGE_DETECTION = 3
CV_CORNER_DETECTION = 4
CV_KEYPOINT_DETECTION = 5

###
## Radio Frequency Transmitter Detection #
###
RF_VALID_ENCODINGS = [
    70963, 70972,
    71107, 71116,
    71427, 71436,
    72963, 72972,
    79107, 79116]

###
# CVFrameRecorder Enumerations #
###

## Codecs
CV_FRAME_RECORDER_MP4V = 'mp4v'
