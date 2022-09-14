import numpy as np
import cv2
import time

cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

elapsed_time = 0

start_time = time.time()

text_x_offset = 20
text_y_offset = 20

while True:
    ret, frame = cap.read()

    if ret:
        elapsed_time = time.time()-start_time
        start_time = time.time()

        cv2.putText(frame, str(round(1/elapsed_time)) + " FPS", (text_x_offset, text_y_offset),
                                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 2)

        cv2.imshow("Frame", frame)

    key = cv2.waitKey(1) & 0xFF

    # if the 'q' key is pressed, stop the loop
    if key == ord("q"):
        break
