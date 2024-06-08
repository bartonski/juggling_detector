# A basic juggling tracker in Python

All CV2 juggling trackers follow the same basic pattern:

# Setup

## Video Capture

~~~ {#video_capture .python .numberLines}
cap = cv2.VideoCapture(FILENAME)
~~~

## Set up object detector

~~~ {#object_detector .python .numberLines startFrom="2"}
object_detector = cv2.createBackgroundSubtractorMOG2(
                    history=DETECTOR_HISTORY,
                    varThreshold=DETECTOR_THRESHOLD)
~~~

## Set globals used in read loop

~~~ {#read_loop_prep .python .numberLines startFrom="5"}
# Get first frame
ret, frame = cap.read()
tracked_objects = []
~~~

# Video read loop

`track()` and `display_in_frame()` are user defined

~~~ {#read_loop .python .numberLines startFrom="8"}
while ret:

    mask = object_detector.apply(frame)

    contours, _ = cv2.findContours( mask,
                                    cv2.RETR_TREE,
                                    cv2.CHAIN_APPROX_SIMPLE )

    tracked_objects=track(tracked_objects, contours)

    frame=display_in_frame(frame, tracked_objects)

    # Create a named window
    cv2.namedWindow("Juggling", cv2.WINDOW_NORMAL)
    cv2.imshow("Juggling", frame)

    key = cv2.waitKey(frame_delay)
    if key == 27:
        break

    ret, frame = cap.read()
~~~

# Free Resources after read loop

~~~ {#post_loop .python .numberLines startFrom="29"}
cap.release()
cv2.destroyAllWindows()
~~~
