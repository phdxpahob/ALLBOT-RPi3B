# Simple demo of of the PCA9685 PWM servo/LED controller library.
# Used to drive the Velleman VR412 of the robot.

from __future__ import division
import time

# Import the PCA9685 module.
import Adafruit_PCA9685


# Uncomment to enable debug output.
#import logging
#logging.basicConfig(level=logging.DEBUG)

# Initialise the PCA9685 using the default address (0x40).
pwm = Adafruit_PCA9685.PCA9685()

# Alternatively specify a different address and/or bus:
#pwm = Adafruit_PCA9685.PCA9685(address=0x41, busnum=2)

# Configure min and max servo pulse lengths
servo_min = 111 #150  # Min pulse length out of 4096
servo_max = 489 #600  # Max pulse length out of 4096


hipFrontLeft = 0
kneeFrontLeft = 1
ankleFrontLeft = 2


hipFrontRight = 4
kneeFrontRight = 5
ankleFrontRight = 6


hipRearLeft = 8
kneeRearLeft = 9
ankleRearLeft = 10


hipRearRight = 12
kneeRearRight = 13
ankleRearRight = 14

def spider_step_forward():
    pwm.set_pwm(kneeRearRight, 0, set_servo_angle(0))

def set_servo_angle(degg):
    if degg > 180:
        degg = 180
    elif degg < 0:
        degg = 0
    servopuls = int(servo_min + (servo_max-servo_min)/180 * degg)
    return servopuls

# Set frequency to 50hz, good for servos.
pwm.set_pwm_freq(50)

