import cv2
import os
import sys
import re
import getopt
import math
import json
argv = sys.argv[1:]

try:
    opts, args = getopt.getopt(
              argv, "s:e:g:a:lmr", [
              "start_frame =", "end_frame =",
              "gray_threshold =", "grey_threshold =",
              "area_threshold =", "area_labels",
              "no_trails", "mask",
              "grid", "grid_spacing =",
              "blur_radius =",
              "detector_history =", "detector_threshold =" ]
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
frame_delay = 1
toggle = [1, 0]
detector_history = 100
detector_threshold = 40
blur_radius = None

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
    elif opt in ['--detector_threshold ']:
        detector_threshold = int(arg)
    elif opt in ['--detector_history ']:
        detector_history = int(arg)
    elif opt in ['--blur_radius ']:
        blur_radius = int(arg)

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
object_detector = cv2.createBackgroundSubtractorMOG2(
                    history=detector_history,
                    varThreshold=detector_threshold)

print( f"size: {width}x{height}")
print( f"video frame count: {frame_count}")
print( f"start_frame: {start_frame}")
print( f"end_frame: {end_frame}")
print( f"selection frame count: {end_frame-start_frame}")
print( f"trails: {trails}")
print( f"show_mask: {show_mask}" )
print( f"grey_threshold: {grey_threshold}" )
print( f"area_threshold: {area_threshold}" )
print( f"area_labels: {area_labels}" )
print( f"grid: {grid}" )
print( f"grid_spacing: {grid_spacing}" )
print( f"grid_width: {grid_width}" )
print( f"detector_threshold: {detector_threshold}")
print( f"detector_history: {detector_history}")

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

def get_center( contour ):
                M = cv2.moments(contour)
                return [ int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]) ]

# May want to center text, see
# https://gist.github.com/xcsrz/8938a5d4a47976c745407fe2788c813a
def object_labels( image, text, center, label_offset, shadow_offset ):
    offset=label_offset-shadow_offset
    cv2.putText(image, f"{text}", (center[0]-offset, center[1]-offset),
                cv2.FONT_HERSHEY_PLAIN, 1, (0, 0, 0), 2 )
    offset=label_offset
    cv2.putText(image, f"{text}", (center[0]-offset, center[1]-offset),
                cv2.FONT_HERSHEY_PLAIN, 1, (0, 255, 255), 2 )

def label( image, text, center, label_offset, shadow_offset ):
    offset=label_offset-shadow_offset
    cv2.putText(image, f"{text}", (center[0]-offset, center[1]-offset),
                cv2.FONT_HERSHEY_PLAIN, 1, (0, 0, 0), 2 )
    offset=label_offset
    cv2.putText(image, f"{text}", (center[0]-offset, center[1]-offset),
                cv2.FONT_HERSHEY_PLAIN, 1, (255, 255, 255), 2 )

print( f"After def. area_labels: {area_labels}")

# frame objects have an object id, a center and a 'seen' field.
last_frame_objects = []  
object_id=0
tracking_threshold=20
def track( contours ):
    #print( f"contours: {contours}")
    frame_objects = []
    global object_id
    global last_frame_objects
    for contour in contours:
        area = cv2.contourArea(contour)
        if area > area_threshold:
            frame_object = {} 
            frame_object["center"]=get_center(contour)
            frame_object["seen"]=False
            frame_object["contour"] = contour
            frame_object["area"] = area
            for lfo in last_frame_objects:
                offset_x = frame_object["center"][0] - lfo["center"][0]
                offset_y = frame_object["center"][1] - lfo["center"][1]
                if math.hypot(offset_x, offset_y) <= tracking_threshold:
                    frame_object["object_id"] = lfo["object_id"]
                    frame_object["seen"] = True
            #print( f"frame_object: {frame_object}")
            frame_objects.append(frame_object) 
    new_frame_objects = []
    for fo in frame_objects:
        if fo["seen"] == False:
            object_id += 1
            fo["object_id"] = object_id
        new_frame_objects.append(fo)
    last_frame_objects = new_frame_objects.copy()
    #print( object_id )
    return new_frame_objects
# Video Read Loop --------------------------------------------------------------

ret, frame = cap.read()

while ret and current_frame <= end_frame:
    if current_frame < start_frame:
        current_frame += 1
        continue
    print( f"current_frame: {current_frame}")
    if blur_radius is not None:
        blur_diameter = blur_radius * 2 + 1
        mask_input = cv2.GaussianBlur(frame, (blur_diameter, blur_diameter), 0)
    else:
        mask_input = frame
    mask = object_detector.apply(mask_input)
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


    tracked_objects=track(contours)
    #print(f"tracked_objects: {tracked_objects}")
    for to in tracked_objects:
        # print(f"to: {to}")
        centers.append(to["center"])
        if trails:
            cv2.drawContours(image, [to["contour"]], -1, (0, 255, 0), 2)
            for center in centers:
                red   = 0xFF
                color = ( 0, 0, red )
                cv2.circle(image, (center[0], center[1]), 2, color, -1)
        cv2.drawContours(image, [to["contour"]], -1, (0, 255, 0), 2)
        # if object_id in to:
        #     oid=to["object_id"]
        #     print("to[object_id]: {oid}")
        #     object_labels( image, to["object_id"], to["center"], 10, 2)
        oid=to["object_id"]
        print(f"to[object_id]: {oid} to[center] {to['center']}")
        object_labels( image, to["object_id"], to["center"], 0, 2)
        if area_labels:
            label( image, to["area"], to["center"], 20, 3 )

    out.write(image)
    cv2.namedWindow(window_label, cv2.WINDOW_NORMAL) # Create a named window
    cv2.moveWindow(window_label, 40,30)              # Move it to (40,30)
    cv2.imshow(window_label, image)

    key = cv2.waitKey(frame_delay)
    if key == 27:
        break
    elif key == ord(' '):
        frame_delay = toggle[frame_delay]
    elif key == ord('f'):
        frame_delay = 0

    ret, frame = cap.read()
    current_frame += 1

cap.release()
out.release()
#cv2.destroyAllWindows()
