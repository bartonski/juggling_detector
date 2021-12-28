# Juggling Detector

An object detection program to show trails of hands and juggling balls while
juggling.

<iframe width="560" height="315" src="https://www.youtube.com/embed/25pxncC-uQY" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>

## Usage

    python3 juggling_detector.py [-s|--start_frame START] [-e|--end_frame] VIDEO FILE

This will play VIDEO FILE, drawing an outline around objects detected in the current frame, as well as the trail of the center of mass of each object, taken over time.

An output video file will be written out to a file that has a file name based on the video file, with `.detector` added before the file extension. For example if VIDEO FILE is `3_balls.mp4`, the output file will be `3_balls.detector.mp4`

The option `-s` or `--start_frame`, with the argument of **START** can be used to specify that object detection should start on frame number **START**, likewise `-e` or `--end_frame` with the argument of **END** will stop detection at **END**.

## Examples

    python3 juggling_detector.py 3_balls.mp4

Track and display objects in `3_balls.mp4`, write output to `3_balls.detector.mp4`


    python3 juggling_detector.py --start_frame 100 --end_frame 1500 3_balls.mp4

Track and display objects in `3_balls.mp4` between frames 100 and 1500, write output to `3_balls.detector.mp4`

## Prerequisites

Requires Python3 and the cv2 library. Running under Ubuntu, you should be able to run

    sudo apt install python3
    sudo apt install pip3
    sudo apt install build-essential
    pip3 install opencv-python

A google search for 'python install cv2 windows 10', 'python install cv2 OSX', etc should give you instruction on installing the cv2 libraries.

Some environements may call python 3 as `python` rather than `python3`.
