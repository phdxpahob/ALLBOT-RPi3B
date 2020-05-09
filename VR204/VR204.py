# Python script for ALLBOT VR204 two-legged standing robot.
# Runs on Raspberry Pi with attached Adafruit PCA9685 PWM servo/LED 
# controller board plugged on the I2C bus. Requires the Adafruit 
# library to be installed on the Pi.

# Credits to Tony DiCola for the Adafruit library &
# Velleman nv for the ALLBOT

# Author: Tsveti Hranov
# License: GPLv3
from __future__ import division
import time
import random

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
# These values are based on the assumptions that pwm frequency is 50 Hz.
# If you intend to use 60Hz uncomment the other values instead.
servo_min = 111 #150  # Min pulse length out of 4096
servo_max = 489 #600  # Max pulse length out of 4096

# Set PWM frequency. 
# You can use 60Hz, but you have to change servo _min & _max.
pwm.set_pwm_freq(50)

def set_servo_angle(degg):
    """ 
    Helper function to calculate the servo pulse value for pwm.set_pwm()
    """
    if degg > 180:
        degg = 180
    elif degg < 0:
        degg = 0
    servopuls = int(servo_min + (servo_max-servo_min)/180 * degg)
    return servopuls

class WBServo:
    """Walking robot servo control class, based on ALLBOT arduino/cpp class"""
    
    def __init__(self, pin, flipped, offset, angle):
        self.flipped = flipped
        self.pin = pin
        self.offset = offset
        self.angle = 180 - angle if flipped else angle 
        self.to_angle = self.angle
        pwm.set_pwm(pin, 0, set_servo_angle(self.angle))
    
    def move(self, to_angle):
        self.to_angle = 180 - to_angle if self.flipped else to_angle
        self.to_angle = self.to_angle - self.offset if self.flipped else self.to_angle + self.offset

def animate(speedms):
    """
    Invoking this function traverses all servos that are set to move 
    synchronously and will move them gradually with time delay "speedms".
    It compares if angle & to_angle and if not, then they are moved with
    a single degree per time delay, until to_angle and angle are equal.
    """
    not_done = True
    while not_done:
        not_done = False
        for i in servos():
            if i.angle != i.to_angle:
                i.angle += 1 if i.angle<i.to_angle else -1
                not_done = True
                pwm.set_pwm(i.pin, 0, set_servo_angle(i.angle))
                # print(i.angle) #DEBUG
        time.sleep(speedms)

def servos():
    """This name list is required for animate() to function"""
    yield hipLeft
    yield hipRight
    yield ankleLeft
    yield ankleRight

# Here are initialized all the joints, Arduino ALLBOT-lib style.
# NAME = WBServo(pin, flipped, offset, init_angle)
hipLeft= WBServo(0, True, 0, 90)
hipRight= WBServo(4, False, 0, 90)

ankleLeft= WBServo(1, True, 0, 90)
ankleRight= WBServo(5, False, 0, 90)

#--------------------------------------------------------------
def chirp(beeps, speed):
    print("chirp not implemented yet", beeps, speed)

#--------------------------------------------------------------
def VR204_standup:
    hipLeft.move(90)
    hipRight.move(90) 
    ankleLeft.move(90)
    ankleRight.move(90)
    animate(0.001)

#--------------------------------------------------------------
def VR204_walkbackward(steps, speed):
    hipLeft.move(130)
    hipRight.move(40) 
    animate(speed)
    
    for i in range(0, steps):
        ankleLeft.move(135)
        animate(speed*2)
        
        ankleRight.move(45)
        animate(speed*2)
        
        ankleLeft.move(90)
        animate(speed*2)
        
        ankleRight.move(90)
        animate(speed*2)
    
    hipLeft.move(90)
    hipRight.move(90) 
    animate(speed)

#--------------------------------------------------------------
def VR204_walkforward(steps, speed):
    hipLeft.move(130)
    hipRight.move(40) 
    animate(speed)
    
    for i in range(0, steps):
        ankleLeft.move(45)
        animate(speed*2)
        
        ankleRight.move(135)
        animate(speed*2)
        
        ankleLeft.move(90)
        animate(speed*2)
        
        ankleRight.move(90)
        animate(speed*2)
    
    hipLeft.move(90)
    hipRight.move(90) 
    animate(speed)

#--------------------------------------------------------------
def VR204_lookright(speed):
    hipLeft.move(45)
    hipRight.move(135)
    animate(speed)
    
    delay(speed/2)
    
    hipLeft.move(90)
    hipRight.move(90)
    animate(speed)

#--------------------------------------------------------------
def VR204_lookleft(speed):
    hipLeft.move(135)
    hipRight.move(45)
    animate(speed)
    
    delay(speed/2)
    
    hipLeft.move(90)
    hipRight.move(90)
    animate(speed)

#--------------------------------------------------------------
def VR204_walkright(steps, speed):
    for i in range(0, steps):
        ankleRight.move(45)
        animate(speed)
        
        ankleLeft.move(135)
        animate(speed)
        
        ankleRight.move(90)
        animate(speed)
        
        ankleLeft.move(90)
        animate(speed)

#--------------------------------------------------------------
def VR204_walkleft(int steps, int speed:
    for i in range(0, steps):
        ankleLeft.move(45)
        animate(speed)
        
        ankleRight.move(135)
        animate(speed)
        
        ankleLeft.move(90)
        animate(speed)
        
        ankleRight.move(90)
        animate(speed)

#--------------------------------------------------------------
def VR204_scared(int shakes, int beeps:
    for i in range(0, shakes):
        ankleLeft.move(45)
        ankleRight.move(45)
        animate(0.010)
        
        ankleLeft.move(135)
        ankleRight.move(135)
        animate(0.010)
    
    ankleLeft.move(90)
    ankleRight.move(90)
    animate(0.010)
    
    chirp(beeps, 0)

#--------------------------------------------------------------
# Initialise the spider robot:
VR204_standup()

# Chirp for ready:
chirp(1, 50)
chirp(1, 255)
chirp(3, 0)

time.sleep(2) # 2 seconds time delay before random actions

print("Ctrl+C to stop...") # The only way to exit...

# Random action infinite loop:
while True:
    time.sleep(random.uniform(0.001, 0.02));
    action = random.randint(0, 17)
    
    if action == 0:
        VR204_lookleft(random.uniform(.001, .0255))
    elif action == 1:
        VR204_lookright(random.uniform(.001, .0255))
    elif action == 2:
        VR204_walkforward(random.randint(2, 10), random.uniform(.001, .015))
    elif action == 3:
        VR204_walkbackward(random.randint(2, 10), random.uniform(.001, .015))
    elif action == 4:
        VR204_walkleft(random.randint(2, 10), random.uniform(.001, .015))
    elif action == 5:
        VR204_walkright(random.randint(2, 10), random.uniform(.001, .015))
    elif action == 6:
        VR204_scared(random.randint(2, 10), random.uniform(.0005, .003))
    elif action == 7:
        chirp(random.randint(1, 30), random.uniform(.0001, .0255))
