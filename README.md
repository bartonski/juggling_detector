# Juggling Detector

A program to detect and track the paths of hands, and props thrown in a juggling pattern.

[Example output](https://www.youtube.com/embed/25pxncC-uQY)

## Usage

    usage: juggling_detector.py [-h] [--start_frame START] [--end_frame END]
                                [--grey_threshold GREY THRESHOLD]
                                [--area_threshold AREA THRESHOLD] [--area_labels]
                                [--no_trails] [--show_mask] [--grid]
                                [--grid_spacing GRID SPACING]
                                [--blur_radius BLUR RADIUS]
                                [--throw_roi_bottom PIXELS FROM TOP]
                                [--detector_history DETECTOR HISTORY]
                                [--tracking_threshold TRACKING THRESHOLD]
                                [--detector_threshold DETECTOR THRESHOLD]
                                [--write_discard_mask] [--write_throw_mask]
                                [--write_left_hand_mask] [--write_right_hand_mask]
                                [--discard_read_mask DISCARD MASK INPUT FILE]
                                [--throw_read_mask THROW MASK INPUT FILE]
                                [--left_hand_read_mask LEFT HAND MASK INPUT FILE]
                                [--right_hand_read_mask RIGHT HAND MASK INPUT FILE]
                                VIDEO FILE

    positional arguments:
    VIDEO FILE              Input video file

    options:
    -h, --help              show this help message and exit
    --start_frame START, -s START
                            Start program at frame #START
    --end_frame END, -e END
                            End program at frame #END
    --grey_threshold GREY THRESHOLD, -g GREY THRESHOLD,
    --gray_threshold GREY THRESHOLD
                            What shades of grey in the detctor mask are counted as
                            objects during object detection
    --area_threshold AREA THRESHOLD, -a AREA THRESHOLD
                            The minimum number of pixels inside an object to be
                            counted during objext detection
    --area_labels, -l       Show the area of each object.
    --no_trails             Do not show the trails showing where the props have
                            been
    --show_mask, --mask, -m
                            Show the gray scale image used by the object detector,
                            instead of the input video.
    --grid, -r              Show horizontal and vertical lines every 100 pixels
    --grid_spacing GRID SPACING
                            Adjust the number of pixels between lines displayed by
                            "--grid"
    --blur_radius BLUR RADIUS
                            Increasing blur radius makes the image blurrier, which
                            may increase the area seen by the object detector
    --throw_roi_bottom PIXELS FROM TOP
                            Bottom edge of of area of interest where props are
                            caught and thrown.
    --detector_history DETECTOR HISTORY
                            Number of frames available for the object detector to
                            look backward during object detection.
    --tracking_threshold TRACKING THRESHOLD
                            Distance in pixels for objects to be tracked from
                            frame to frame
    --detector_threshold DETECTOR THRESHOLD
                            Adjust the sensitivity of the object detector
    --write_discard_mask    Write discard mask to png file.
    --write_throw_mask      Write throw trails mask to png file.
    --write_left_hand_mask
                            Write left hand trails mask to png file.
    --write_right_hand_mask
                            Write right hand trails mask to png file.
    --discard_read_mask DISCARD MASK INPUT FILE
                            Png file where locations of objects to ignore are
                            colored white
    --throw_read_mask THROW MASK INPUT FILE
                            Png file where locations of throw objects are colored
                            white
    --left_hand_read_mask LEFT HAND MASK INPUT FILE
                            Png file where locations of left hand objects are
                            colored white
    --right_hand_read_mask RIGHT HAND MASK INPUT FILE
                            Png file where locations of right hand objects are
                            colored white

## Understanding the object detector

The juggling detector works by comparing video frames in succession. Areas
that stay the same are ignored. For each frame, difference are written
to a grey scale image called the 'mask'. Contiguous areas that have a
pixel count larger than `--area_threshold` counted as 'things' by the
detector. The value of `--detector_threshold` can be tweaked to make
the detector more or less sensitive (lowering the threshold makes the
detector more sensitive, which means more objects will be detected,
but increases the chances of a false positive). The `--grey_threshold`
is the minimum grey value that an area must have to be counted as part of
the area used by `--area_threshold`. `--grey_threshold` may be between 0
(black) to 255 (Only count areas on the mask that are entirely white). If
`--blur_radius` is specified, video frames are blurred before object
detection occurs. This may or may not help with detection. The higher the
value of `--blur_radius`, the more the input frames are blurred. Blurred
images will probably show as shades of gray, so `--grey_threshold`
may need to be lowered.

See Tips for getting good object detection.

## Examples

    python3 juggling_detector.py 3_balls.mp4

Track and display objects in `3_balls.mp4`, write output to `3_balls.detector.mp4`

    python3 juggling_detector.py --start_frame 100 --end_frame 1500 3_balls.mp4

Track and display objects in `3_balls.mp4` between frames 100 and 1500, write output to `3_balls.detector.mp4`

## Tips for getting good object detection

* Make sure that your camera is steady. *Any* movement of the camera will throw off the object detection
* Use `--start_frame` and `--end_frame` to exclude non-juggling video.
* Use balls that have good color contrast with the background, including your shirt and your face
* Use even lighting that does not cast shadows that can be picked up as extraneous movement
* Start by using the `--no_trails` and `--area_labels` options. Stop the animation by pressing the space bar, and frame advance by pressing <kbd>f</kbd>. Area labels are printed in white with a black drop shadow. This is the area picked up by object detector. This is useful for determining the value of `--area_threshold`. If the image is noisy and you are seeing objects that you don't want to track, increase the area threshold so that the area of the noise is below the threshold. If the props are not detected at a certain part of the throw, decrease the area threshold until the area of the prop is above the threshold. Increasing the blur radius (possibly in conjunction with the grey threshold) may increase the area of detected props.

## Tips for object tracking

* Shooting in slow-mo (60 fps or higher) makes object tracking more accurate.
* `--throw_roi_bottom` is the bottom edge of the 'Region of Interest' for throws and catches. It is the number of pixels from the top of the picture down to the lowest point where the props appear after having left the hand. Try to set this *above* the trails of the hands. This will keep the hands from being tracked as props.
* Use the `--grid` option to display horizontal and vertical lines every 100 pixels, to help determine the correct value of `--throw_roi_bottom`. You can use `--grid_spacing` to adjust the number of pixels between lines.

## Installation

Click the green **Code** button above, then click **Download Zip**. This will put the file `juggling_detector-main.zip` in your Downloads folder.

### Ubuntu

(This may work for Debian and other debian based distributions; I haven't tested it)

Open a terminal and run

    unzip ~/Downloads/juggling_detector-main.zip 
    sudo apt install python3
    sudo apt install pip3
    sudo apt install build-essential
    pip3 install opencv-python

To test, run

    cd ~/juggling_detector-main/
    python3 juggling_detector.py [YOUR VIDEO FILE]

### Windows 10/Windows 11

TODO: Finish installation instructions for Windows

* Download python -- Find **Download Windows installer (64-bit)** under Stable Releases on [Python Releases for Windows](https://www.python.org/downloads/windows/). Download and run the installer.

A google search for 'python install cv2 windows 10', 'python install cv2 OSX', etc should give you instruction on installing the cv2 libraries.

Some environements may call python 3 as `python` rather than `python3`.
