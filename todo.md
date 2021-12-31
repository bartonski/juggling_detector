### Update Readme.md

### Implement `--help`

### Refactor Video Read Loop 

### Implement frame rate.

This will be in one of the following formats:

* NN fps -- output frame rate is set explicitly
* NN %   -- output frame rate is a percentage of input frame rate
* NN x   -- output frame rate is a multiple of input frame rate

### Implement `--contour_color`

### Implement `--trail_color`

### Implement `--detector_history`

### Implement `--detector_threshold`

### Implement import and export of configuration

### Write trails to separate image

Use `cv2.bitwise_and` to merge trails with image
(see <https://youtu.be/WQeoO7MI0Bs?t=4347> )
This should drastically improve performance.

### Add object tracking. See https://www.youtube.com/watch?v=GgGro5IV-cs

### Add Regions of interest

* left throw
* right throw
* left hand
* right hand
* left catch
* right catch.

### Get timing and location for the start of each throw

### Find average throw position and velocity for left and right throws

### Draw average left and right hand throws
