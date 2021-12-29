import cv2
import os
import sys
import re
import getopt
argv = sys.argv[1:]

start_frame = 0
end_frame = None
show_mask = False

try:
    opts, args = getopt.getopt(argv, "s:e:m", 
                                ["start_frame =",
                                "end_frame =",
                                "mask"])
    
except:
    print("Error")

for opt, arg in opts:
    if opt in ['-s', '--start_frame']:
        start_frame = arg
    elif opt in ['-e', '--end_frame']:
        end_frame = arg
    elif opt in ['-m', '--mask']:
        show_mask = True

filename = str(sys.argv[-1])
current_frame = 0

cap = cv2.VideoCapture(filename)
width      = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
height     = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
frame_rate = int(cap.get(cv2.CAP_PROP_FPS))
frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

if end_frame is None:
    end_frame = frame_count
#r = re.compile('(.*)\.([^.]+$)')
#basename = r.sub( '', filename )
result = re.search( '(.*)\.([^.]+$)', filename )
basename, extension = result.groups()
label="detector"
output_file=f"{basename}.{label}.{extension}"
#print( f"basename: {basename}, extension: {extension}")

# Object detection from stable camera
object_detector = cv2.createBackgroundSubtractorMOG2(history=100, varThreshold=40)


out = cv2.VideoWriter(
        output_file,
        cv2.VideoWriter_fourcc('M','J','P','G'),
        frame_rate/2,
        (width, height)
      )

print( f"size: {width}x{height}");

ret, frame = cap.read()

centers = []

while ret and current_frame <= end_frame:
    if current_frame >= start_frame:
        mask = object_detector.apply(frame)
        _, mask = cv2.threshold( mask, 254, 255, cv2.THRESH_BINARY )
        contours, _ = cv2.findContours( mask,
                                        cv2.RETR_TREE,
                                        cv2.CHAIN_APPROX_SIMPLE )
        for cnt in contours:
            area = cv2.contourArea(cnt)
            if area > 400:
                M = cv2.moments(cnt)
                current = [int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"])]
                centers.append( current )
                cv2.drawContours(frame, [cnt], -1, (0, 255, 0), 2)
                for center in centers:
                    red   = 0xFF
                    color = ( 0, 0, red )
                    cv2.circle(frame, (center[0], center[1]), 2, color, -1)
                cv2.drawContours(frame, [cnt], -1, (0, 255, 0), 2)
        if show_mask:
            cv2.namedWindow("Mask")        # Create a named window
            cv2.moveWindow("Mask", 40,30)  # Move it to (40,30)
            cv2.imshow("Mask", mask)
        else:
            out.write(frame)
            cv2.namedWindow("Frame")        # Create a named window
            cv2.moveWindow("Frame", 40,30)  # Move it to (40,30)
            cv2.imshow("Frame", frame)

        key = cv2.waitKey(1)
        if key == 27:
            break

    ret, frame = cap.read()
    current_frame += 1

cap.release()
out.release()
#cv2.destroyAllWindows()
