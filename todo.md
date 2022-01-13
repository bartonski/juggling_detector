### Update Readme.md

* Write "Understanding the object detector" section.

### Implement `--help`

### Refactor Video Read Loop 

### Implement frame rate.

This will be in one of the following formats:

* NN fps -- output frame rate is set explicitly
* NN %   -- output frame rate is a percentage of input frame rate
* NN x   -- output frame rate is a multiple of input frame rate

### Implement `--contour_color`

### Implement `--trail_color`

### Implement import and export of configuration

### Write trails to separate image

Use `cv2.bitwise_and` to merge trails with image
(see <https://youtu.be/WQeoO7MI0Bs?t=4347> )
This should drastically improve performance.

### Add Region of interest

* throw-catch ( bottom is configurable, should be able to set top, left and right )
* left hand
* right hand

### Write trail-mask to image

Trails will be written as white pixels in a black and white image.

### Read trail-masks from images

* This allows for really fine grained control of what is a prop, what's a hand, and what's garbage.
* 3 possible trail-masks: prop (throw), left hand, right hand. A paint program can be used to mask out pixels that are not part of the relevant path by coloring them black.

### Get timing and location for the start of each throw

### Get location of the peak of each throw

* The peak and start of through can be used to calculate acceleration in pixels/frame^2. Because we know frame rate in FPS, we can convert pixels to feet, inches, or meters.

### Find average throw position and velocity for left and right throws

* Left and right throws can be determined by the direction of the throw. (not a good assumption for cross handed / mills mess, but we have to start somewhere...)

### Draw average left and right hand throws
