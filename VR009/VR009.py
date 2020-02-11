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
wheelFrontLeft = 2


hipFrontRight = 4
kneeFrontRight = 5
wheelFrontRight = 6


hipRearLeft = 8
kneeRearLeft = 9
wheelRearLeft = 10


hipRearRight = 12
kneeRearRight = 13
wheelRearRight = 14

def set_servo_angle(degg):
    if degg > 180:
        degg = 180
    elif degg < 0:
        degg = 0
    servopuls = int(servo_min + (servo_max-servo_min)/180 * degg)
    return servopuls
