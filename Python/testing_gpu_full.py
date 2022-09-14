# https://learnopencv.com/getting-started-opencv-cuda-module/
import numpy as np
import cv2
import imutils

hardware = "gpu"

#https://stackoverflow.com/questions/10948589/choosing-the-correct-upper-and-lower-hsv-boundaries-for-color-detection-withcv/48367205#48367205
colors_hsv = {#"red":([0, 82, 39], [179, 255, 224]), #Red technically might need a range in the 170 area
              "green":([43, 57, 50], [66, 255,255]),
              "yellow":([23, 140, 81], [32, 255, 255]),
              "orange":([1, 46, 33], [13, 255, 255]),
              "blue":([93, 68, 69], [116, 255, 170]),
              "brown": ([0, 0, 42], [27, 136, 129])
              }

cap = cv2.VideoCapture(0)
record = False

frame_width = int(cap.get(3))
frame_height = int(cap.get(4))

text_x_offset = -20
text_y_offset = -20
min_size = 10

fps = 30

contours = {}

writer = cv2.VideoWriter('tracking_video.mp4', cv2.VideoWriter_fourcc(*'DIVX'),
                         fps, (frame_width,frame_height))

# allow the camera or video file to warm up
#time.sleep(2.0)

while True:
    # grab the current frame
    ret, frame = cap.read()

    # proceed if frame reading was successful

    if hardware == "gpu":
        if ret:
            # resize frame
            frame = cv2.resize(previous_frame, (480, 360))

            # upload resized frame to GPU
            gpu_frame = cv2.cuda_GpuMat()
            gpu_frame.upload(frame)

            # convert to gray
            previous_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

            # upload pre-processed frame to GPU
            gpu_previous = cv2.cuda_GpuMat()
            gpu_previous.upload(previous_frame)

            # create gpu_hsv output for optical flow
            gpu_hsv = cv2.cuda_GpuMat(gpu_frame.size(), cv2.CV_32FC3)
            gpu_hsv_8u = cv2.cuda_GpuMat(gpu_frame.size(), cv2.CV_8UC3)

            gpu_h = cv2.cuda_GpuMat(gpu_frame.size(), cv2.CV_32FC1)
            gpu_s = cv2.cuda_GpuMat(gpu_frame.size(), cv2.CV_32FC1)
            gpu_v = cv2.cuda_GpuMat(gpu_frame.size(), cv2.CV_32FC1)

            # set saturation to 1
            gpu_s.upload(np.ones_like(previous_frame, np.float32))

    elif hardware == "cpu":
        if not ret:
            print("No frame")
            break

        # resize the frame, blur it, and convert it to HSV
        #Resizing breaks video recording
        #frame = imutils.resize(frame, width=600)
        blurred = cv2.GaussianBlur(frame, (11, 11), 0)
        hsv = cv2.cvtColor(blurred, cv2.COLOR_BGR2HSV)

        total_mask = np.zeros((frame.shape[0], frame.shape[1]), dtype=np.int8)

        for name in colors_hsv:
            lower = np.array(colors_hsv[name][0], dtype = "uint8")
            upper = np.array(colors_hsv[name][1], dtype = "uint8")

            mask = cv2.inRange(hsv, lower, upper)
            mask = cv2.erode(mask, None, iterations=3)
            mask = cv2.dilate(mask, None, iterations=3)

            # find contours in the mask
            contours = cv2.findContours(mask.copy().astype(np.uint8), cv2.RETR_EXTERNAL,
                                    cv2.CHAIN_APPROX_SIMPLE)
            contours = imutils.grab_contours(contours)

            # only proceed if at least one contour was found
            if len(contours) > 0:
                # find the largest contour in the mask, then use
                # it to compute the minimum enclosing circle and
                # centroid
                for distinct_contour in contours:
                    c = distinct_contour
                    ((x, y), radius) = cv2.minEnclosingCircle(c)
                    M = cv2.moments(c)

                    # only proceed if the radius meets a minimum size
                    if radius > min_size:
                        if M['m00'] != 0:
                            cx = int(M['m10'] / M['m00'])
                            cy = int(M['m01'] / M['m00'])
                            cv2.drawContours(frame, [distinct_contour], -1, (0, 255, 0), 2)
                            #cv2.circle(frame, (cx, cy), 7, (0, 0, 255), -1)
                            cv2.putText(frame, name, (cx + text_x_offset, cy + text_y_offset),
                                       cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 2)
                            cv2.circle(frame, (cx, cy), 5, (255,255,255), -1)

        # show the frame to our screen
        cv2.imshow("Frame", frame)
        if record:
            writer.write(frame)
        key = cv2.waitKey(1) & 0xFF

        # if the 'q' key is pressed, stop the loop
        if key == ord("q"):
            writer.release()
            break