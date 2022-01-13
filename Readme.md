# Juggling Detector

A program to detect and track the paths of hands, and props thrown in a juggling pattern.

[Example output](https://www.youtube.com/embed/25pxncC-uQY)

## Usage

    python3 juggling_detector.py [-s|--start_frame START] [-e|--end_frame END]
                                 [-g|--gray_threshold|--grey_threshold] GREY THRESHOLD
                                 [-a|--area_threshold] AREA THRESHOLD
                                 [-l|--area_labels] [--no_trails] [-m|--mask] [-r|--grid]
                                 [--grid_spacing] GRID SPACING
                                 [--detector_threshold] DETECTOR THRESHOLD
                                 [--detector_history] DETECTOR HISTORY
                                 [--blur_radius] BLUR RADIUS
                                 [--throw_roi_bottom] PIXELS FROM TOP
				 VIDEO FILE

## Options


* `-s START` or `--start_frame START`
    * start program at frame #START
* `-e` or `--end_frame`
    * stop program at frame #END
* `-g GREY THRESHOLD` or `--gray_threshold GREY THRESHOLD` or `--grey_threshold GREY THRESHOLD`
    * What shades of gray in the detctor mask are counted as objects during object detection (see Understanding the object detector)
* `-a AREA THRESHOLD` or `--area_threshold AREA THRESHOLD`
    * What is the minimum number of pixels inside an object to be counted during objext detection (see Understanding the object detector)
* `-l` or `--area_labels`
    * Show the area of each object.
* `--no_trails`
    * Do not show the trails showing where the props have been
* `-m` or `--mask`
    * Show the gray scale image used by the object detector, instead of the input video.
* `-r` or `--grid`
    * Show horizonatl and vertical lines every 100 pixels
* `--grid_spacing GRID SPACING`
    * Adjust the number of pixels between lines displayed by `--grid`
* `--detector_threshold DETECTOR THRESHOLD`
    * Adjust the sensitivity of the object detector
* `--detector_history DETECTOR HISTORY`
    * Number of frames available for the object detector to look backward during object detection.
* `--blur_radius BLUR RADIUS`
    * Increasing blur radius makes the image blurrier, which may increase the area seen by the object detector.
* `--throw_roi_bottom PIXELS FROM TOP`
    * Bottom edge of of area of interest where props are caught and thrown.

## Understanding the object detector

[TODO: discuss detector mask, gray threshold, area threshold, detector threshold, detector history and blur radius]

See Tips for getting good object detection.

## Examples

    python3 juggling_detector.py 3_balls.mp4

Track and display objects in `3_balls.mp4`, write output to `3_balls.detector.mp4`


    python3 juggling_detector.py --start_frame 100 --end_frame 1500 3_balls.mp4

Track and display objects in `3_balls.mp4` between frames 100 and 1500, write output to `3_balls.detector.mp4`

## Tips for getting good object detection

* Make sure that your camera is steady. *Any* movement of the camera will throw off the object detection
* Use balls that have good color contrast with the background, including your shirt and your face
* Use even lighting that does not cast shadows that can be picked up as extraneous movement
* Start by using the `--no_trails` and `--area_labels` options. Stop the animation by pressing the space bar, and frame advance by pressing <kbd>f</kbd>. Area labels are printed in white with a black drop shadow. This is the area picked up by object detector. This is useful for determining the value of `--area_threshold`. If the image is noisy and you are seeing objects that you don't want to track, increase the area threshold so that the area of the noise is below the threshold. If the props are not detected at a certain part of the throw, decrease the area threshold until the area of the prop is above the threshold. Increasing the blur radius (possibly in conjunction with the grey threshold) may increase the area of detected props.

## Tips for object tracking

* Shooting in slow-mo (more than 60 fps) makes object tracking more accurate.
* `--throw_roi_bottom` is the bottom edge of the 'Region of Interest' for throws and catches. It is the number of pixels from the top of the picture down to the lowest point where the props appear after having left the hand. Try to set this *above* the trails of the hands. This will keep the hands from being tracked as props.
* Use the `--grid` option to display horizontal and vertical lines every 100 pixels, to help determine the correct value of `--throw_roi_bottom`. You can use `--grid_spacing` to adjust the number of pixels between lines.

## Prerequisites

Requires Python3 and the cv2 library. Running under Ubuntu, you should be able to run

    sudo apt install python3
    sudo apt install pip3
    sudo apt install build-essential
    pip3 install opencv-python

A google search for 'python install cv2 windows 10', 'python install cv2 OSX', etc should give you instruction on installing the cv2 libraries.

Some environements may call python 3 as `python` rather than `python3`.
