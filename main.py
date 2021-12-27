import cv2
import os
import sys
import re

filename = str(sys.argv[1])
frames = int(sys.argv[2])
if frames is None:
    frames = 1000000
current_frame = 0

cap = cv2.VideoCapture(filename)
r = re.compile('\.[^.]+$')
basename = r.sub( '', filename )
#basename

# Object detection from stable camera
object_detector = cv2.createBackgroundSubtractorMOG2(history=100, varThreshold=40)

width      = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
height     = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
frame_rate = int(cap.get(cv2.CAP_PROP_FPS))

out = cv2.VideoWriter(
        'juggling_detection.mp4',
        cv2.VideoWriter_fourcc('M','J','P','G'),
        frame_rate/2,
        (width, height)
      )

print( f"size: {width}x{height}");

ret, frame = cap.read()

centers = []

while ret and current_frame <= frames:
    mask = object_detector.apply(frame)
    _, mask = cv2.threshold(mask, 254, 255, cv2.THRESH_BINARY)
    contours, _ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    for cnt in contours:
        area = cv2.contourArea(cnt)
        if area > 400:
            M = cv2.moments(cnt)
            current = [int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"])]
            centers.append( current )
            #cX = int(M["m10"] / M["m00"])
            #cY = int(M["m01"] / M["m00"])
            cv2.drawContours(frame, [cnt], -1, (0, 255, 0), 2)
            for center in centers:
                red   = 0xFF
                color = ( 0, 0, red )
                cv2.circle(frame, (center[0], center[1]), 2, color, -1)
            cv2.drawContours(frame, [cnt], -1, (0, 255, 0), 2)
    print( f"current frame: {current_frame}")
    out.write(frame)

    cv2.namedWindow("Frame")        # Create a named window
    cv2.moveWindow("Frame", 40,30)  # Move it to (40,30)
    cv2.imshow("Frame", frame)
    #cv2.imshow("Mask", mask)

    key = cv2.waitKey(1)
    if key == 27:
        break

    ret, frame = cap.read()
    current_frame += 1

cap.release()
out.release()
#cv2.destroyAllWindows()
