This is the code for the VELLEMAN six-legged two joints robot VR612

![VELLEMAN six-legged with two joints robot VR612](http://images.velleman.eu/manuals/allbot/arduino-allbot/04/003.jpg "VR612") 

You might need to configure the pins, depending on the configuration of the legs. This is done in the section after the comment:
```
# NAME = WBServo(pin, flipped, offset, init_angle)
```

Simple way to run the demo is through `ssh`. Simply navigate to the folder where the script is and run 
```
path/to/allbot/rpi3b/$: python VR612.py
```
or
```
$ path/to/allbot/rpi3b/VR612.py
```
to run the demo with random actions. If you get a "VR612.py: Permission denided" error message, just mark the script as executable with:
```
$ chmod +x path/to/allbot/rpi3b/VR612.py
```
The script could be used as a starting point to code a ROS controlled robot, web based teleop, local wireless joystick on the Pi and so on.
Initially the experimentation can be done using `ssh` and calling the functions to see the robot's behaivior and then code a communication routine.

Have fun experimenting!
