import cv2
import os
import sys
import re
import getopt
argv = sys.argv[1:]

try:
    opts, args = getopt.getopt(
              argv, "s:e:g:a:lmr", [
              "start_frame =", "end_frame =",
              "gray_threshold =", "grey_threshold =",
              "area_threshold =", "area_labels",
              "no_trails", "mask",
              "grid", "grid_spacing =" ]
          )
except:
    print("Error")

print(f"opts: {opts}")

# Default Values ---------------------------------------------------------------

start_frame = 0
end_frame = None
show_mask = False
trails = True
grey_threshold = 255
area_threshold = 100
area_labels = False
trails = True
grid = False
grid_spacing = 100
grid_width = 2
grid_color = ( 128, 128, 128 )

# Parse Arguments --------------------------------------------------------------

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
    elif opt in ['-r', '--grid']:
        grid = True
    elif opt in [ '--grid_spacing ']:
        grid_spacing = int(arg)

# Set-up -----------------------------------------------------------------------

## Input Video file

filename = str(sys.argv[-1])

cap = cv2.VideoCapture(filename)
width      = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
height     = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
frame_rate = int(cap.get(cv2.CAP_PROP_FPS))
frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

## Output Video file

result = re.search( '(.*)\.([^.]+$)', filename )
basename, extension = result.groups()
label="detector"
output_file=f"{basename}.{label}.{extension}"

out = cv2.VideoWriter(
        output_file, cv2.VideoWriter_fourcc('m','p','4','v'),
        frame_rate/2, (width, height)
      )

if end_frame is None:
    end_frame = frame_count

# Object detection from stable camera
object_detector = cv2.createBackgroundSubtractorMOG2(history=100, varThreshold=40)

print( f"size: {width}x{height}");
print( f"start_frame: {start_frame}");
print( f"end_frame: {end_frame}");
print( f"trails: {trails}");

current_frame = 0
centers = []

# Helper Functions for Video Read Loop -----------------------------------------

def show_grid( image ):
    # Draw horizontal lines
    for y in range(0, height, grid_spacing):
        cv2.line(image, ( 0, y), (width, y), grid_color, grid_width  )
    # Draw vertical lines
    for x in range(0, width, grid_spacing):
        cv2.line(image, ( x, 0), (x, height), grid_color, grid_width  )

def get_center( image, contour ):
                M = cv2.moments(contour)
                return [ int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]) ]

def area_labels( image, area, label_offset, shadow_offset ):
    offset=label_offset-shadow_offset
    cv2.putText(image, f"{area}", (current[0]-offset, current[1]-offset),
                cv2.FONT_HERSHEY_PLAIN, 1, (0, 0, 0), 2 )
    offset=label_offset
    cv2.putText(image, f"{area}", (current[0]-offset, current[1]-offset),
                cv2.FONT_HERSHEY_PLAIN, 1, (255, 255, 255), 2 )


# Video Read Loop --------------------------------------------------------------

ret, frame = cap.read()

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
    
        if grid:
            show_grid( image )   

        for cnt in contours:
            area = cv2.contourArea(cnt)
            if area > area_threshold:
                # Add tracking here.
                current = get_center( image, cnt )
                centers.append( current )
                if trails:
                    cv2.drawContours(image, [cnt], -1, (0, 255, 0), 2)
                    for center in centers:
                        red   = 0xFF
                        color = ( 0, 0, red )
                        cv2.circle(image, (center[0], center[1]), 2, color, -1)
                cv2.drawContours(image, [cnt], -1, (0, 255, 0), 2)
                if area_labels:
                    area_labels( image, area, 20, 3 )

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
