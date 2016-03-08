import numpy as np
import cv2
from time import gmtime, strftime
from collections import deque


def isMoving(frame, sensibility):
    """Check if threshold image detect any motion

        Args:
            frame: an array result of the cv2.threshold() function

        Returns:
            True for motion detected
            False for motion non detected

        Raises:

    """
    ##calculates the amount of "motion"
    motionQuantity = sum(sum(frame/255))
    if (motionQuantity > sensibility):
        return True
    return False


##VideoCapture object
cap = cv2.VideoCapture(0)
##BackgroundSubtractor object
fgbg = cv2.createBackgroundSubtractorMOG2()
##CODEC used for recording
fourcc = cv2.VideoWriter_fourcc(*'XVID')
##VideoWriter object
out = cv2.VideoWriter('output.avi',fourcc, 20.0, (640,480))
##Font object
font = cv2.FONT_HERSHEY_PLAIN
##Create deque
preRecording = deque(maxlen=40)
##Variables
record = False
sensibility = 1000

while(1):
    ##reads the frame
    ret, frame = cap.read()

    ##creates a blur to reduce noise
    blur = cv2.GaussianBlur(frame, (15,15),0)
    ##generates mask
    fgmask = fgbg.apply(blur)
    ##thresholds the mask
    thresh = cv2.threshold(fgmask, 25, 255, cv2.THRESH_BINARY)[1]

    preRecording.append(frame)

    if (isMoving(thresh,sensibility)):
        record = True
        counter = 60

    if(record or counter > 0):
        ##Writes the date and time in the frame
        ##putText(frame,text,location,font,size,color,thickness,aliasing)
        cv2.putText(preRecording.pop(), strftime("%Y-%m-%d %H:%M:%S", gmtime()), (10,20), font, 1.4, (0,0,0), 1, cv2.LINE_AA)
        ##Writes frame into video
        out.write(frame)
        counter -=1

    if(counter == 0):
        record = False

    ##Show images
    cv2.imshow('frame',frame)
    #cv2.imshow('fgmask',fgmask)
    #cv2.imshow('thresh',thresh)


    ##Press ESC to exit
    k = cv2.waitKey(30) & 0xff
    if k == 27:
        break

cap.release()
cv2.destroyAllWindows()
out.release()