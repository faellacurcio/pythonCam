#!/usr/bin/env python 

import cv2

if __name__ == "__main__":
    # find the webcam
    cap = cv2.VideoCapture(0)
    w = cap.get(cv2.CAP_PROP_FRAME_WIDTH)
    h = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
    # video recorder
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter('output.mp4', fourcc, 15.0, (int(w), int(h)))

    # record video
    while (cap.isOpened()):
        ret, frame = cap.read()
        if ret:
            out.write(frame)
            cv2.imshow('Video Stream', frame)

        else:
            break

    cap.release()
    out.release()
    cv2.destroyAllWindows()
