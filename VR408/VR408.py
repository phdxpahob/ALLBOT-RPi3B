# Simple demo of of the PCA9685 PWM servo/LED controller library.
# This will move channel 0 from min to max position repeatedly.
# Author: Tony DiCola
# License: Public Domain
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

hipFrontRight = 4
kneeFrontRight = 5

hipRearLeft = 8
kneeRearLeft = 9

hipRearRight = 12
kneeRearRight = 13

def set_servo_angle(degg):
    if degg > 180:
        degg = 180
    elif degg < 0:
        degg = 0
    servopuls = int(servo_min + (servo_max-servo_min)/180 * degg)
    return servopuls

def reset_spider():
    pwm.set_pwm(kneeRearRight, 0, set_servo_angle(45))
    pwm.set_pwm(kneeFrontLeft, 0, set_servo_angle(135))
    pwm.set_pwm(kneeFrontRight, 0, set_servo_angle(135))
    pwm.set_pwm(kneeRearLeft, 0, set_servo_angle(45))
    pwm.set_pwm(hipRearRight, 0, set_servo_angle(45))
    pwm.set_pwm(hipFrontLeft, 0, set_servo_angle(45))
    pwm.set_pwm(hipFrontRight, 0, set_servo_angle(135))
    pwm.set_pwm(hipRearLeft, 0, set_servo_angle(135))

def spider_step_forward():
    pwm.set_pwm(kneeRearRight, 0, set_servo_angle(80))
    pwm.set_pwm(kneeFrontLeft, 0, set_servo_angle(100))
    time.sleep(.07) # sleep times could be replaced.
    
    pwm.set_pwm(hipRearRight, 0, set_servo_angle(100))
    pwm.set_pwm(hipFrontLeft, 0, set_servo_angle(110))
    time.sleep(.06)
    
    pwm.set_pwm(kneeRearRight, 0, set_servo_angle(30))
    pwm.set_pwm(kneeFrontLeft, 0, set_servo_angle(150))
    time.sleep(.03)
    
    pwm.set_pwm(hipRearRight, 0, set_servo_angle(45))
    pwm.set_pwm(hipFrontLeft, 0, set_servo_angle(45))
    time.sleep(.07)
    
    pwm.set_pwm(kneeRearRight, 0, set_servo_angle(45))
    pwm.set_pwm(kneeFrontLeft, 0, set_servo_angle(135))
    time.sleep(.03)
    
    pwm.set_pwm(kneeRearLeft, 0, set_servo_angle(100))
    pwm.set_pwm(kneeFrontRight, 0, set_servo_angle(80))
    time.sleep(.07)
    
    pwm.set_pwm(hipRearLeft, 0, set_servo_angle(80))
    pwm.set_pwm(hipFrontRight, 0, set_servo_angle(80))
    time.sleep(.06)
    
    pwm.set_pwm(kneeRearLeft, 0, set_servo_angle(30))
    pwm.set_pwm(kneeFrontRight, 0, set_servo_angle(150))
    time.sleep(.1)
    
    pwm.set_pwm(hipRearLeft, 0, set_servo_angle(135))
    pwm.set_pwm(hipFrontRight, 0, set_servo_angle(135))
    time.sleep(.07)
    
    pwm.set_pwm(kneeRearLeft, 0, set_servo_angle(45))
    pwm.set_pwm(kneeFrontRight, 0, set_servo_angle(135))
    time.sleep(.03)
    
def spider_step_backward():
    pwm.set_pwm(kneeRearRight, 0, set_servo_angle(80))
    pwm.set_pwm(kneeFrontLeft, 0, set_servo_angle(100))    
    time.sleep(.03)
    
    pwm.set_pwm(hipRearRight, 0, set_servo_angle(20))
    pwm.set_pwm(hipFrontLeft, 0, set_servo_angle(80))    
    time.sleep(.05)
    
    pwm.set_pwm(kneeRearRight, 0, set_servo_angle(30))
    pwm.set_pwm(kneeFrontLeft, 0, set_servo_angle(150))    
    time.sleep(.07)
    
    pwm.set_pwm(hipRearRight, 0, set_servo_angle(45))
    pwm.set_pwm(hipFrontLeft, 0, set_servo_angle(45))    
    time.sleep(.03)
    
    pwm.set_pwm(kneeRearRight, 0, set_servo_angle(45))
    pwm.set_pwm(kneeFrontLeft, 0, set_servo_angle(135))    
    time.sleep(.03)
    
    pwm.set_pwm(kneeRearLeft, 0, set_servo_angle(80))
    pwm.set_pwm(kneeFrontRight, 0, set_servo_angle(100))    
    time.sleep(.05)
    
    pwm.set_pwm(hipRearLeft, 0, set_servo_angle(160))
    pwm.set_pwm(hipFrontRight, 0, set_servo_angle(100))    
    time.sleep(.07)
    
    pwm.set_pwm(kneeRearLeftt, 0, set_servo_angle(45))
    pwm.set_pwm(kneeFrontRight, 0, set_servo_angle(135))    
    time.sleep(.03)
    
    pwm.set_pwm(hipRearLeft, 0, set_servo_angle(45))
    pwm.set_pwm(hipFrontRight, 0, set_servo_angle(135))    
    time.sleep(.03)
    
    pwm.set_pwm(kneeRearLeft, 0, set_servo_angle(45))
    pwm.set_pwm(kneeFrontRight, 0, set_servo_angle(135))    
    time.sleep(.03)
    
def spider_step_right():
    pwm.set_pwm(kneeRearLeft, 0, set_servo_angle(80))
    pwm.set_pwm(kneeFrontRight, 0, set_servo_angle(80))
    time.sleep(.07)
    
    pwm.set_pwm(hipRearLeft, 0, set_servo_angle(0))
    pwm.set_pwm(hipFrontRight, 0, set_servo_angle(90))
    time.sleep(.06)
    
    pwm.set_pwm(kneeRearLeft, 0, set_servo_angle(30))
    pwm.set_pwm(kneeFrontRight, 0, set_servo_angle(30))
    time.sleep(.03)
    
    pwm.set_pwm(hipRearLeft, 0, set_servo_angle(45))
    pwm.set_pwm(hipFrontRight, 0, set_servo_angle(45))
    time.sleep(.07)
    
    pwm.set_pwm(kneeRearLeft, 0, set_servo_angle(45))
    pwm.set_pwm(kneeFrontRight, 0, set_servo_angle(45))
    time.sleep(.03)
    
    pwm.set_pwm(kneeRearRight, 0, set_servo_angle(80))
    pwm.set_pwm(kneeFrontLeft, 0, set_servo_angle(80))
    time.sleep(.07)
    
    pwm.set_pwm(hipRearRight, 0, set_servo_angle(90))
    pwm.set_pwm(hipFrontLeft, 0, set_servo_angle(0))
    time.sleep(.06)
    
    pwm.set_pwm(kneeRearRight, 0, set_servo_angle(30))
    pwm.set_pwm(kneeFrontLeft, 0, set_servo_angle(30))
    time.sleep(.1)
    
    pwm.set_pwm(hipRearRight, 0, set_servo_angle(45))
    pwm.set_pwm(hipFrontLeft, 0, set_servo_angle(45))
    time.sleep(.07)
    
    pwm.set_pwm(kneeRearRight, 0, set_servo_angle(45))
    pwm.set_pwm(kneeFrontLeft, 0, set_servo_angle(45))
    time.sleep(.03)
    
def spider_step_left():
    pwm.set_pwm(kneeRearRight, 0, set_servo_angle(80))
    pwm.set_pwm(kneeFrontLeft, 0, set_servo_angle(100))
    time.sleep(.07) # sleep times could be replaced.
    
    pwm.set_pwm(hipRearRight, 0, set_servo_angle(0))
    pwm.set_pwm(hipFrontLeft, 0, set_servo_angle(90))
    time.sleep(.06)
    
    pwm.set_pwm(kneeRearRight, 0, set_servo_angle(30))
    pwm.set_pwm(kneeFrontLeft, 0, set_servo_angle(150))
    time.sleep(.03)
    
    pwm.set_pwm(hipRearRight, 0, set_servo_angle(45))
    pwm.set_pwm(hipFrontLeft, 0, set_servo_angle(45))
    time.sleep(.07)
    
    pwm.set_pwm(kneeRearRight, 0, set_servo_angle(45))
    pwm.set_pwm(kneeFrontLeft, 0, set_servo_angle(135))
    time.sleep(.03)
    
    pwm.set_pwm(kneeRearLeft, 0, set_servo_angle(100))
    pwm.set_pwm(kneeFrontRight, 0, set_servo_angle(80))
    time.sleep(.07)
    
    pwm.set_pwm(hipRearLeft, 0, set_servo_angle(90))
    pwm.set_pwm(hipFrontRight, 0, set_servo_angle(0))
    time.sleep(.06)
    
    pwm.set_pwm(kneeRearLeft, 0, set_servo_angle(30))
    pwm.set_pwm(kneeFrontRight, 0, set_servo_angle(150))
    time.sleep(.1)
    
    pwm.set_pwm(hipRearLeft, 0, set_servo_angle(135))
    pwm.set_pwm(hipFrontRight, 0, set_servo_angle(135))
    time.sleep(.07)
    
    pwm.set_pwm(kneeRearLeft, 0, set_servo_angle(45))
    pwm.set_pwm(kneeFrontRight, 0, set_servo_angle(135))
    time.sleep(.03)
    
def spider_turn_left():
    pwm.set_pwm(kneeRearRight, 0, set_servo_angle(80))
    pwm.set_pwm(kneeFrontLeft, 0, set_servo_angle(100))
    time.sleep(.07) # sleep times could be replaced.
    
    pwm.set_pwm(hipRearRight, 0, set_servo_angle(90))
    pwm.set_pwm(hipFrontLeft, 0, set_servo_angle(90))
    time.sleep(.06)
    
    pwm.set_pwm(kneeRearRight, 0, set_servo_angle(30))
    pwm.set_pwm(kneeFrontLeft, 0, set_servo_angle(150))
    time.sleep(.03)
    
    pwm.set_pwm(hipRearRight, 0, set_servo_angle(45))
    pwm.set_pwm(hipFrontLeft, 0, set_servo_angle(45))
    time.sleep(.07)
    
    pwm.set_pwm(kneeRearRight, 0, set_servo_angle(45))
    pwm.set_pwm(kneeFrontLeft, 0, set_servo_angle(135))
    time.sleep(.03)
    
    pwm.set_pwm(kneeRearLeft, 0, set_servo_angle(100))
    pwm.set_pwm(kneeFrontRight, 0, set_servo_angle(80))
    time.sleep(.07)
    
    pwm.set_pwm(hipRearLeft, 0, set_servo_angle(0))
    pwm.set_pwm(hipFrontRight, 0, set_servo_angle(0))
    time.sleep(.06)
    
    pwm.set_pwm(kneeRearLeft, 0, set_servo_angle(30))
    pwm.set_pwm(kneeFrontRight, 0, set_servo_angle(150))
    time.sleep(.1)
    
    pwm.set_pwm(hipRearLeft, 0, set_servo_angle(135))
    pwm.set_pwm(hipFrontRight, 0, set_servo_angle(135))
    time.sleep(.07)
    
    pwm.set_pwm(kneeRearLeft, 0, set_servo_angle(45))
    pwm.set_pwm(kneeFrontRight, 0, set_servo_angle(135))
    time.sleep(.03)
    
    
# Set frequency to 60hz, good for servos.
pwm.set_pwm_freq(50)

print('Reset spider position...')
reset_spider()
time.sleep(2)

print('Walk forward...')
spider_step_forward()
time.sleep(2)
