import cv2
import os
import sys
import re
import getopt
argv = sys.argv[1:]

start_frame = 0
end_frame = None
show_mask = False
trails = True
grey_threshold = 255
area_threshold = 100
area_labels = False
trails = True

# TODO: implement frame rate.
#       This will be in one of the following formats:
#           NN fps -- output frame rate is set explicitly
#           NN %   -- output frame rate is a percentage of input frame rate
#           NN x   -- output frame rate is a multiple of input frame rate

# TODO: Implement '--contour_color'

# TODO: Implement '--trail_color'

# TODO: Implement import and export of configuration

# TODO: Write trails to separate image
#       Use cv2.bitwise_and to merge trails with image
#       (see https://youtu.be/WQeoO7MI0Bs?t=4347 )
#       This should drastically improve performance.

# TODO: I think I can use HSV masking to isolate the colors of balls and hands,
#       which should make image recognition easier and more accurate.

try:
    opts, args = getopt.getopt(argv, "s:e:g:a:lm", 
                                ["start_frame =", "end_frame =",
                                "gray_threshold =", "grey_threshold =",
                                "area_threshold =", "area_labels",
                                "no_trails", "mask"])
    
except:
    print("Error")

print(f"opts: {opts}")

for opt, arg in opts:
    if opt in ['-s', '--start_frame ']:
        start_frame = int(arg)
    elif opt in ['-e', '--end_frame ']:
        end_frame = int(arg)
    elif opt in ['-g', '--gray_threshold ', '--grey_threshold ']:
        grey_threshold = int(arg)
    elif opt in ['-a', '--area_threshold ']:
        area_threshold = int(arg)
    elif opt in ['-l', '--area_labels']:
        area_labels = True
    elif opt in [ '--no_trails']:
        trails = False
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
        cv2.VideoWriter_fourcc('m','p','4','v'),
        frame_rate/2,
        (width, height)
      )

print( f"size: {width}x{height}");
print( f"start_frame: {start_frame}");
print( f"end_frame: {end_frame}");
print( f"trails: {trails}");

ret, frame = cap.read()

centers = []

while ret and current_frame <= end_frame:
    if current_frame >= start_frame:
        mask = object_detector.apply(frame)
        _, mask = cv2.threshold( mask, grey_threshold-1, grey_threshold,
                                 cv2.THRESH_BINARY )
        contours, _ = cv2.findContours( mask,
                                        cv2.RETR_TREE,
                                        cv2.CHAIN_APPROX_SIMPLE )
        if show_mask:
            window_label = "Mask"
            image = mask
        else:
            window_label = "Frame"
            image = frame

        for cnt in contours:
            area = cv2.contourArea(cnt)
            if area > area_threshold:
                M = cv2.moments(cnt)
                center_x = int(M["m10"] / M["m00"])
                center_y = int(M["m01"] / M["m00"])
                current = [center_x, center_y]
                centers.append( current )
                if trails:
                    cv2.drawContours(image, [cnt], -1, (0, 255, 0), 2)
                    for center in centers:
                        red   = 0xFF
                        color = ( 0, 0, red )
                        cv2.circle(image, (center[0], center[1]), 2, color, -1)
                cv2.drawContours(image, [cnt], -1, (0, 255, 0), 2)
                if area_labels:
                    cv2.putText(image, f"{area}", (center_x - 18, center_y - 18),
                                cv2.FONT_HERSHEY_PLAIN, 1, (0, 0, 0), 2 )
                    cv2.putText(image, f"{area}", (center_x - 20, center_y - 20),
                                cv2.FONT_HERSHEY_PLAIN, 1, (255, 255, 255), 2 )

        out.write(image)
        cv2.namedWindow(window_label)        # Create a named window
        cv2.moveWindow(window_label, 40,30)  # Move it to (40,30)
        cv2.imshow(window_label, image)

        key = cv2.waitKey(1)
        if key == 27:
            break

    ret, frame = cap.read()
    current_frame += 1

cap.release()
out.release()
#cv2.destroyAllWindows()
