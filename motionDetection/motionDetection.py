# import numpy as np
import cv2
from time import localtime, strftime
from collections import deque
# loggex.py
import logging

# ========= Logger Setup =========
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
fh = logging.FileHandler('events.log')
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
fh.setFormatter(formatter)
logger.addHandler(fh)

videoExt = ".avi"
videoFolder = "./videos/"


def getTime():
    return strftime("%Y-%m-%d %H:%M:%S", localtime())


def isMoving(frame, sensibility):
    """Check if threshold image detect any motion

        Args:
            frame: an array result of the cv2.threshold() function

        Returns:
            True for motion detected
            False for motion non detected

        Raises:

    """
    # #calculates the amount of "motion"
    motionQuantity = sum(sum(frame / 255))
    if (motionQuantity > sensibility):
        return True
    return False


logger.info("Motion Detection started")

# #VideoCapture object
cap = cv2.VideoCapture(0)
# #BackgroundSubtractor object
fgbg = cv2.createBackgroundSubtractorMOG2()
# #CODEC used for recording
fourcc = cv2.VideoWriter_fourcc(*'XVID')
w = cap.get(cv2.CAP_PROP_FRAME_WIDTH)
h = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)   
# #VideoWriter object
out = cv2.VideoWriter(videoFolder + getTime() + videoExt, fourcc, 15.0, (int(w), int(h)))
# #Font object
font = cv2.FONT_HERSHEY_PLAIN
# #Create deque
preRecording = deque(maxlen=20)
# #Variables
record = False
sensibility = 1000

while(1):
    # #reads the frame
    ret, frame = cap.read()

    # #creates a blur to reduce noise
    blur = cv2.GaussianBlur(frame, (15, 15), 0)
    # #generates mask
    fgmask = fgbg.apply(blur)
    # #thresholds the mask
    thresh = cv2.threshold(fgmask, 25, 255, cv2.THRESH_BINARY)[1]
    # #Add frame to deque
    preRecording.append(frame)

    if (isMoving(thresh, sensibility)):
        record = True
        counter = 50

    if(record or counter > 0):
        # #Writes the date and time in the frame
        # #putText(frame,text,location,font,size,color,thickness,aliasing)
        aux = preRecording.popleft()
        cv2.putText(aux, getTime(), (10, 20), font, 1.4, (0, 0, 0), 1, cv2.LINE_AA)
        cv2.putText(frame, "*", (300, 20), font, 1.4, (0, 0, 0), 1, cv2.LINE_AA)
        # #Writes frame into video
        out.write(aux)
        counter -= 1

    # Once it reaches the last frame prepares a new videoWriter with a new timestamp
    if(counter == 1):
        out = cv2.VideoWriter(videoFolder + getTime() + videoExt, fourcc, 15.0, (int(w), int(h)))
        counter -= 1
        record = False

    # #Show images
    cv2.imshow('frame', frame)
    # cv2.imshow('fgmask',fgmask)
    # cv2.imshow('thresh',thresh)

    # #Press ESC to exit
    k = cv2.waitKey(30) & 0xff
    if k == 27:
        break

logger.info("Shutdown motion detection")
cap.release()
out.release()
cv2.destroyAllWindows()
