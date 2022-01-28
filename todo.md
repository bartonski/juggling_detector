### Refactor Video Read Loop 

### Implement frame rate.

This will be in one of the following formats:

* NN fps -- output frame rate is set explicitly
* NN %   -- output frame rate is a percentage of input frame rate
* NN x   -- output frame rate is a multiple of input frame rate

### Implement `--contour_color`

### Implement `--trail_color`

### Implement import and export of configuration

### Add Region of interest

* throw-catch ( bottom is configurable, should be able to set top, left and right )
* left hand
* right hand

### Get timing and location for the start of each throw

### Get location of the peak of each throw

* The peak and start of through can be used to calculate acceleration in pixels/frame^2. Because we know frame rate in FPS, we can convert pixels to feet, inches, or meters.

### Find average throw position and velocity for left and right throws

* Left and right throws can be determined by the direction of the throw. (not a good assumption for cross handed / mills mess, but we have to start somewhere...)

### Draw average left and right hand throws
