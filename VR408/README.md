This is the code for the standard VELLEMAN four-legged robot VR408.

You might need to configure the pins, depending on the configuration of the legs. This is done in the section after the comment:
```
# NAME = WBServo(pin, flipped, offset, init_angle)
```

Simple way to run the demo is through `ssh`. Simply navigate to the folder where the script is and run 
```python VR408.py```
to run the demo with random actions. The script could be used as a starting point to code a ROS controlled robot, web based teleop, local wireless joystick on the Pi and so on.
Initially the experimentation can be done using `ssh` and calling the functions to see the robot's behaivior
