# Python script for ALLBOT VR408 Four-legged robot.
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
    yield hipFrontLeft
    yield hipFrontRight
    yield hipRearLeft
    yield hipRearRight
    yield kneeFrontLeft
    yield kneeFrontRight
    yield kneeRearLeft
    yield kneeRearRight

# Here are initialized all the joints, Arduino ALLBOT-lib style.
# NAME = WBServo(pin, flipped, offset, init_angle)
hipFrontLeft = WBServo(0, True, 0, 45)
kneeFrontLeft = WBServo(1, True, 0, 45)

hipFrontRight = WBServo(4, False, 0, 45)
kneeFrontRight = WBServo(5, True, 0, 45)

hipRearLeft = WBServo(8, False, 0, 45)
kneeRearLeft = WBServo(9, False, 0, 45)

hipRearRight = WBServo(12, True, 0, 45)
kneeRearRight = WBServo(13, False, 0, 45)

def VR408_reset_spider():
    """Stand-still position of the ALLBOT VR408"""
    kneeRearRight.move(45)
    kneeFrontLeft.move(45)
    kneeFrontRight.move(45)
    kneeRearLeft.move(45)
    hipRearRight.move(45)
    hipFrontLeft.move(45)
    hipFrontRight.move(45)
    hipRearLeft.move(45)
    animate(0.001)

#--------------------------------------------------------------
def chirp(beeps, speed):
    print("chirp not implemented yet", beeps, speed)

#--------------------------------------------------------------
def VR408_waverearleft(waves, speed):
    kneeRearLeft.move(180)
    animate(speed)
    
    for i in range(0, waves):
        hipRearLeft.move(0)
        animate(speed)
        
        hipRearLeft.move(65)
        animate(speed)
        
        hipRearLeft.move(0)
        animate(speed)
        
        hipRearLeft.move(45)
        animate(speed)
    
    kneeRearLeft.move(45)
    animate(speed)

#--------------------------------------------------------------
def VR408_waverearright(waves, speed):
    kneeRearRight.move(180)
    animate(speed)
    
    for i in range(0, waves):
        hipRearRight.move(0)
        animate(speed)
        
        hipRearRight.move(65)
        animate(speed)
        
        hipRearRight.move(0)
        animate(speed)
        
        hipRearRight.move(45)
        animate(speed)
    
    kneeRearRight.move(45)
    animate(speed)

#--------------------------------------------------------------
def VR408_wavefrontright(waves, speed):
    kneeFrontRight.move(180)
    animate(speed)
    
    for i in range(0, waves):
        hipFrontRight.move(0)
        animate(speed)
        
        hipFrontRight.move(65)
        animate(speed)
        
        hipFrontRight.move(0)
        animate(speed)
        
        hipFrontRight.move(45)
        animate(speed)
    
    kneeFrontRight.move(45)
    animate(speed)

#--------------------------------------------------------------
def VR408_wavefrontleft(waves, speed):
    kneeFrontLeft.move(180)
    animate(speed)
    
    for i in range(0, waves):
        hipFrontLeft.move(0)
        animate(speed)
        
        hipFrontLeft.move(65)
        animate(speed)
        
        hipFrontLeft.move(0)
        animate(speed)
        
        hipFrontLeft.move(45)
        animate(speed)
    
    kneeFrontLeft.move(45)
    animate(speed)

#--------------------------------------------------------------
def VR408_scared(shakes, beeps):
    kneeFrontRight.move(0)
    kneeRearRight.move(0)
    kneeFrontLeft.move(0)
    kneeRearLeft.move(0)
    animate(0.005)
    
    for i in range(0, shakes):
        hipRearRight.move(80)
        hipRearLeft.move(10)
        hipFrontRight.move(10)
        hipFrontLeft.move(80)
        animate(0.01);
        
        hipRearLeft.move(80)
        hipRearRight.move(10)
        hipFrontLeft.move(10)
        hipFrontRight.move(80)
        animate(0.005)
    
    hipRearRight.move(45)
    hipRearLeft.move(45)
    hipFrontRight.move(45)
    hipFrontLeft.move(45)
    animate(0.02)
    
    chirp(beeps, 0)
    
    kneeFrontRight.move(45)
    kneeRearRight.move(45)
    kneeFrontLeft.move(45)
    kneeRearLeft.move(45)
    animate(0.0075);

#--------------------------------------------------------------
def VR408_leanbackward(speed):
    kneeRearLeft.move(90)
    kneeRearRight.move(90)
    animate(speed)
    
    time.sleep(speed/2)
    
    kneeRearLeft.move(45)
    kneeRearRight.move(45)
    animate(speed)

#--------------------------------------------------------------
def VR408_leanleft(speed):
    kneeFrontLeft.move(90)
    kneeRearLeft.move(90)
    animate(speed)
    
    time.sleep(speed/2)
    
    kneeFrontLeft.move(45)
    kneeRearLeft.move(45)
    animate(speed)

#--------------------------------------------------------------
def VR408_leanright(speed):
    kneeFrontRight.move(90)
    kneeRearRight.move(90)
    animate(speed)
    
    time.sleep(speed/2)
    
    kneeFrontRight.move(45)
    kneeRearRight.move(45)
    animate(speed)

#--------------------------------------------------------------
def VR408_leanforward(speed):
    kneeFrontLeft.move(90)
    kneeFrontRight.move(90)
    animate(speed)
    
    time.sleep(speed/2)
    
    kneeFrontLeft.move(45)
    kneeFrontRight.move(45)
    animate(speed)

#--------------------------------------------------------------
def VR408_lookleft(speed):
    hipRearLeft.move(80)
    hipRearRight.move(10)
    hipFrontLeft.move(10)
    hipFrontRight.move(80)
    animate(speed)
    
    time.sleep(speed/2)
    
    hipRearRight.move(45)
    hipRearLeft.move(45)
    hipFrontRight.move(45)
    hipFrontLeft.move(45)
    animate(speed)

#--------------------------------------------------------------
def VR408_lookright(speed):
    hipRearRight.move(80)
    hipRearLeft.move(10)
    hipFrontRight.move(10)
    hipFrontLeft.move(80)
    animate(speed)
    
    time.sleep(speed/2)
    
    hipRearRight.move(45)
    hipRearLeft.move(45)
    hipFrontRight.move(45)
    hipFrontLeft.move(45)
    animate(speed)

#--------------------------------------------------------------
def VR408_walkforward(steps, speed):
    for i in range(0, steps):
        kneeRearRight.move(80)
        kneeFrontLeft.move(80)
        animate(speed)
        
        hipRearRight.move(80)
        hipFrontLeft.move(20)
        animate(speed)
        
        kneeRearRight.move(30)
        kneeFrontLeft.move(30)
        animate(speed)
        
        hipRearRight.move(45)
        hipFrontLeft.move(45)
        animate(speed)
        
        kneeRearRight.move(45)
        kneeFrontLeft.move(45)
        animate(speed)
        
        kneeRearLeft.move(80)
        kneeFrontRight.move(80)
        animate(speed)
        
        hipRearLeft.move(80)
        hipFrontRight.move(20)
        animate(speed)
        
        kneeRearLeft.move(30)
        kneeFrontRight.move(30)
        animate(speed)
        
        hipRearLeft.move(45)
        hipFrontRight.move(45)
        animate(speed)
        
        kneeRearLeft.move(45)
        kneeFrontRight.move(45)
        animate(speed)

#--------------------------------------------------------------
def VR408_walkbackward(steps, speed):
    for i in range(0, steps):
        kneeRearRight.move(80)
        kneeFrontLeft.move(80)
        animate(speed)
        
        hipRearRight.move(20)
        hipFrontLeft.move(80)
        animate(speed)
        
        kneeRearRight.move(30)
        kneeFrontLeft.move(30)
        animate(speed)
        
        hipRearRight.move(45)
        hipFrontLeft.move(45)
        animate(speed)
        
        kneeRearRight.move(45)
        kneeFrontLeft.move(45)
        animate(speed)
        
        kneeRearLeft.move(80)
        kneeFrontRight.move(80)
        animate(speed)
        
        hipRearLeft.move(20)
        hipFrontRight.move(80)
        animate(speed)
        
        kneeRearLeft.move(30)
        kneeFrontRight.move(30)
        animate(speed)
        
        hipRearLeft.move(45)
        hipFrontRight.move(45)
        animate(speed)
        
        kneeRearLeft.move(45)
        kneeFrontRight.move(45)
        animate(speed)

#--------------------------------------------------------------
def VR408_walkright(steps, speed):
    for i in range(0, steps):
        kneeRearLeft.move(80)
        kneeFrontRight.move(80)
        animate(speed)
        
        hipRearLeft.move(0)
        hipFrontRight.move(90)
        animate(speed)
        
        kneeRearLeft.move(30)
        kneeFrontRight.move(30)
        animate(speed)
        
        hipRearLeft.move(45)
        hipFrontRight.move(45)
        animate(speed)
        
        kneeRearLeft.move(45)
        kneeFrontRight.move(45)
        animate(speed)
         
        kneeRearRight.move(80)
        kneeFrontLeft.move(80)
        animate(speed)
        
        hipRearRight.move(90)
        hipFrontLeft.move(0)
        animate(speed)
        
        kneeRearRight.move(30)
        kneeFrontLeft.move(30)
        animate(speed)
        
        hipRearRight.move(45)
        hipFrontLeft.move(45)
        animate(speed)
        
        kneeRearRight.move(45)
        kneeFrontLeft.move(45)
        animate(speed)

#--------------------------------------------------------------
def VR408_walkleft(steps, speed):
    for i in range(0, steps):
        kneeRearRight.move(80)
        kneeFrontLeft.move(80)
        animate(speed)
        
        hipRearRight.move(90)
        hipFrontLeft.move(90)
        animate(speed)
        
        kneeRearRight.move(30)
        kneeFrontLeft.move(30)
        animate(speed)
        
        hipRearRight.move(45)
        hipFrontLeft.move(45)
        animate(speed)
        
        kneeRearRight.move(45)
        kneeFrontLeft.move(45)
        animate(speed)
        
        kneeRearLeft.move(80)
        kneeFrontRight.move(80)
        animate(speed)
        
        hipRearLeft.move(0)
        hipFrontRight.move(0)
        animate(speed)
        
        kneeRearLeft.move(30)
        kneeFrontRight.move(30)
        animate(speed)
        
        hipRearLeft.move(45)
        hipFrontRight.move(45)
        animate(speed)
        
        kneeRearLeft.move(45)
        kneeFrontRight.move(45)
        animate(speed)

#--------------------------------------------------------------
def VR408_turnleft(steps, speed):
    for i in range(0, steps):
        kneeRearRight.move(80)
        kneeFrontLeft.move(80)
        animate(speed)
        
        hipRearRight.move(90)
        hipFrontLeft.move(90)
        animate(speed)
        
        kneeRearRight.move(30)
        kneeFrontLeft.move(30)
        animate(speed)
        
        hipRearRight.move(45)
        hipFrontLeft.move(45)
        animate(speed)
        
        kneeRearRight.move(45)
        kneeFrontLeft.move(45)
        animate(speed)
        
        kneeRearLeft.move(80)
        kneeFrontRight.move(80)
        animate(speed)
        
        hipRearLeft.move(0)
        hipFrontRight.move(0)
        animate(speed)
        
        kneeRearLeft.move(30)
        kneeFrontRight.move(30)
        animate(speed)
        
        hipRearLeft.move(45)
        hipFrontRight.move(45)
        animate(speed)
        
        kneeRearLeft.move(45)
        kneeFrontRight.move(45)
        animate(speed)

#--------------------------------------------------------------
def VR408_turnright(steps, speed):
    for i in range(0, steps):
        kneeRearRight.move(80)
        kneeFrontLeft.move(80)
        animate(speed)
        
        hipRearRight.move(90)
        hipFrontLeft.move(90)
        animate(speed)
        
        kneeRearRight.move(30)
        kneeFrontLeft.move(30)
        animate(speed)
        
        hipRearRight.move(45)
        hipFrontLeft.move(45)
        animate(speed)
        
        kneeRearRight.move(45)
        kneeFrontLeft.move(45)
        animate(speed)
        
        kneeRearLeft.move(80)
        kneeFrontRight.move(80)
        animate(speed)
        
        hipRearLeft.move(0)
        hipFrontRight.move(0)
        animate(speed)
        
        kneeRearLeft.move(30)
        kneeFrontRight.move(30)
        animate(speed)
        
        hipRearLeft.move(45)
        hipFrontRight.move(45)
        animate(speed)
        
        kneeRearLeft.move(45)
        kneeFrontRight.move(45)
        animate(speed)

# Initialise the spider robot:
VR408_reset_spider()

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
        VR408_leanforward(random.uniform(.001, .0255))
    elif action == 1:
        VR408_leanbackward(random.uniform(.001, .0255))
    elif action == 2:
        VR408_leanleft(random.uniform(.001, .0255))
    elif action == 3:
        VR408_leanright(random.uniform(.001, .0255))
    elif action == 4:
        VR408_lookleft(random.uniform(.001, .0255))
    elif action == 5:
        VR408_lookright(random.uniform(.001, .0255))
    elif action == 6:
        VR408_turnleft(random.randint(1, 5), random.uniform(.001, .0255))
    elif action == 7:
        VR408_turnright(random.randint(1, 5), random.uniform(.001, .0255))
    elif action == 8:
        VR408_walkforward(random.randint(2, 10), random.uniform(.001, .015))
    elif action == 9:
        VR408_walkbackward(random.randint(2, 10), random.uniform(.001, .015))
    elif action == 10:
        VR408_walkleft(random.randint(2, 10), random.uniform(.001, .015))
    elif action == 11:
        VR408_walkright(random.randint(2, 10), random.uniform(.001, .015))
    elif action == 12:
        VR408_scared(random.randint(2, 10), random.uniform(.0005, .003))
    elif action == 13:
        VR408_chirp(random.randint(1, 30), random.uniform(.0001, .0255))
    elif action == 14:
        VR408_wavefrontright(random.randint(1, 5), random.uniform(.0025, .01))
    elif action == 15:
        VR408_wavefrontleft(random.randint(1, 5), random.uniform(.0025, .01))
    elif action == 16:
        VR408_waverearright(random.randint(1, 5), random.uniform(.0025, .01))
    elif action == 17:
        VR408_waverearleft(random.randint(1, 5), random.uniform(.0025, .01))
