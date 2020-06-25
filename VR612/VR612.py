# Python script for ALLBOT VR612 Six-legged-two-joint robot.
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
    yield hipMiddleLeft
    yield hipRearLeft
    yield hipFrontRight
    yield hipMiddleRight
    yield hipRearRight
    yield kneeFrontLeft
    yield kneeMiddleLeft
    yield kneeRearLeft
    yield kneeFrontRight
    yield kneeMiddleRight
    yield kneeRearRight

# Here are initialized all the joints, Arduino ALLBOT-lib style.
# NAME = WBServo(pin, flipped, offset, init_angle)

hipFrontLeft = WBServo(0, True, 0, 45)
hipMiddleLeft = WBServo(1, True, 0, 90)
hipRearLeft = WBServo(2, True, 0, 45)

hipFrontRight = WBServo(4, True, 0, 45)
hipMiddleRight = WBServo(5, True, 0, 90)
hipRearRight = WBServo(6, True, 0, 45)

kneeFrontLeft = WBServo(8, True, 0, 20)
kneeMiddleLeft = WBServo(9, True, 0, 20)
kneeRearLeft = WBServo(10, True, 0, 20)

kneeFrontRight = WBServo(12, True, 0, 20)
kneeMiddleRight = WBServo(13, True, 0, 20)
kneeRearRight = WBServo(14, True, 0, 20)

def VR612_reset_spider():
    """Stand-still position of the ALLBOT VR408"""
    kneeFrontRight.move(20)
    kneeRearRight.move(20)
    kneeMiddleRight.move(20)
    
    kneeFrontLeft.move(20)
    kneeRearLeft.move(20)
    kneeMiddleLeft.move(20)
    
    hipFrontRight.move(45)
    hipRearRight.move(45)
    hipMiddleRight.move(90)
    
    hipFrontLeft.move(45)
    hipRearLeft.move(45)
    hipMiddleLeft.move(90)
    animate(0.001)

#--------------------------------------------------------------
def chirp(beeps, speed):
    print("chirp not implemented yet", beeps, speed)

#--------------------------------------------------------------
def VR612_scared(shakes, beeps):
    kneeFrontRight.move(0)
    kneeMiddleRight.move(0)
    kneeRearRight.move(0)
    kneeFrontLeft.move(0)
    kneeMiddleLeft.move(0)
    kneeRearLeft.move(0) 
    animate(.005)
    
    for i in range(0, shakes): 
        hipRearRight.move(80)
        hipMiddleRight.move(65)
        hipRearLeft.move(5)
        hipFrontRight.move(5)
        hipMiddleLeft.move(115)
        hipFrontLeft.move(80)
        animate(.010)
        
        hipRearLeft.move(80)
        hipMiddleRight.move(115)
        hipRearRight.move(5)
        hipFrontLeft.move(5)
        hipMiddleLeft.move(65)
        hipFrontRight.move(80)
        animate(.005)
    
    hipRearRight.move(45)
    hipMiddleRight.move(90)
    hipRearLeft.move(45)
    hipFrontRight.move(45)
    hipMiddleLeft.move(90)
    hipFrontLeft.move(45)
    animate(0.02)
    
    chirp(beeps, 0)
    
    kneeFrontRight.move(20)
    kneeMiddleRight.move(20)
    kneeRearRight.move(20)
    kneeFrontLeft.move(20)
    kneeMiddleLeft.move(20)
    kneeRearLeft.move(20)
    animate(.0075)

#--------------------------------------------------------------
def VR612_turnleft(steps, speed):
    for i in range(0, steps): 
        kneeFrontLeft.move(50)
        kneeRearLeft.move(50)
        kneeMiddleRight.move(50)    
        animate(speed)
        
        hipFrontLeft.move(80)
        hipRearLeft.move(5)
        hipMiddleRight.move(65)    
        animate(speed)
        
        kneeFrontLeft.move(20)
        kneeRearLeft.move(20)
        kneeMiddleRight.move(20)    
        animate(speed)
        
        kneeFrontRight.move(50)
        kneeRearRight.move(50)
        kneeMiddleLeft.move(50)    
        animate(speed)
        
        hipFrontRight.move(5)
        hipRearRight.move(80)
        hipMiddleLeft.move(115)   
        animate(speed)
        
        kneeFrontRight.move(20)
        kneeRearRight.move(20)
        kneeMiddleLeft.move(20)    
        animate(speed)
        
        hipFrontLeft.move(45)
        hipRearLeft.move(45)
        hipMiddleRight.move(90)
        hipFrontRight.move(45)
        hipRearRight.move(45)
        hipMiddleLeft.move(90)    
        animate(speed)

#--------------------------------------------------------------
def VR612_turnright(steps, speed):
    for i in range(0, steps): 
        kneeFrontLeft.move(50)
        kneeRearLeft.move(50)
        kneeMiddleRight.move(50)    
        animate(speed)
        
        hipFrontLeft.move(5)
        hipRearLeft.move(80)
        hipMiddleRight.move(115)    
        animate(speed)
        
        kneeFrontLeft.move(20)
        kneeRearLeft.move(20)
        kneeMiddleRight.move(20)    
        animate(speed)
        
        kneeFrontRight.move(50)
        kneeRearRight.move(50)
        kneeMiddleLeft.move(50)    
        animate(speed)
        
        hipFrontRight.move(80)
        hipRearRight.move(5)
        hipMiddleLeft.move(65)    
        animate(speed)
        
        kneeFrontRight.move(20)
        kneeRearRight.move(20)
        kneeMiddleLeft.move(20)    
        animate(speed)
        
        hipFrontLeft.move(45)
        hipRearLeft.move(45)
        hipMiddleRight.move(90)
        hipFrontRight.move(45)
        hipRearRight.move(45)
        hipMiddleLeft.move(90)    
        animate(speed)

#--------------------------------------------------------------
def VR612_waverearleft(int waves, int speed):
    kneeRearLeft.move(180)
    animate(speed)
    
    for i in range(0, waves): 
        hipRearLeft.move(0)
        animate(speed/2)
        
        hipRearLeft.move(65)
        animate(speed/2)
        
        hipRearLeft.move(0)
        animate(speed/2)
        
        hipRearLeft.move(45)
        animate(speed/2)
    
    kneeRearLeft.move(20)
    animate(speed)

#--------------------------------------------------------------
def VR612_waverearright(waves, speed):
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
    
    kneeRearRight.move(20)
    animate(speed)

#--------------------------------------------------------------
def VR612_wavefrontright(waves, speed):
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
    
    kneeFrontRight.move(20)
    animate(speed)

#--------------------------------------------------------------
def VR612_wavefrontleft(waves, speed):
    kneeFrontLeft.move(180)
    animate(speed)
    
    for i in range(0, waves):
        .move(hipFrontLeft0)
        animate(speed)
        
        .move(hipFrontLeft65)
        animate(speed)
        
        hipFrontLeft.move(0)
        animate(speed)
        
        hipFrontLeft.move(45)
        animate(speed)
    
    kneeFrontLeft.move(20)
    animate(speed)

#--------------------------------------------------------------
def VR612_walkright(steps, speed):
    for i in range(0, steps):
        kneeFrontLeft.move(50)
        kneeRearRight.move(50)
        animate(speed/2)
        
        hipFrontLeft.move(10)
        hipRearRight.move(80)
        animate(speed)
        
        kneeFrontLeft.move(20)
        kneeRearRight.move(20)
        animate(speed/2)
        
        kneeFrontRight.move(50)
        kneeRearLeft.move(50)
        animate(speed/2)
        
        hipFrontRight.move(80)
        hipRearLeft.move(10)
        animate(speed)
        
        kneeFrontRight.move(20)
        kneeRearLeft.move(20)
        animate(speed/2)
        
        kneeMiddleRight.move(50)
        kneeMiddleLeft.move(50)
        animate(speed/2)
        
        hipFrontLeft.move(75)
        hipFrontRight.move(15)
        hipRearLeft.move(75)
        hipRearRight.move(15)
        animate(speed) 
        
        kneeMiddleRight.move(20)
        kneeMiddleLeft.move(20)
        animate(speed/2)
        
        kneeFrontLeft.move(50)
        kneeRearRight.move(50)
        animate(speed/2)
        
        hipFrontLeft.move(45)
        hipRearRight.move(45)
        animate(speed)
        
        kneeFrontLeft.move(20)
        kneeRearRight.move(20)
        animate(speed/2)
        
        kneeFrontRight.move(50)
        kneeRearLeft.move(50)
        animate(speed/2)
        
        hipFrontRight.move(45)
        hipRearLeft.move(45)
        animate(speed)
        
        kneeFrontRight.move(20)
        kneeRearLeft.move(20)
        animate(speed/2)

#--------------------------------------------------------------
def VR612_walkleft(steps, speed):
    for i in range(0, steps): 
        kneeFrontLeft.move(50)
        kneeRearRight.move(50)
        animate(speed/2)
        
        hipFrontLeft.move(80)
        hipRearRight.move(10)
        animate(speed)
        
        kneeFrontLeft.move(20)
        kneeRearRight.move(20)
        animate(speed/2)
        
        kneeFrontRight.move(50)
        kneeRearLeft.move(50)
        animate(speed/2)
        
        hipFrontRight.move(10)
        hipRearLeft.move(80)
        animate(speed)
        
        kneeFrontRight.move(20)
        kneeRearLeft.move(20)
        animate(speed/2)
        
        kneeMiddleRight.move(50)
        kneeMiddleLeft.move(50)
        animate(speed/2)
        
        hipFrontLeft.move(15)
        hipFrontRight.move(75)
        hipRearLeft.move(15)
        hipRearRight.move(75)
        animate(speed) 
        
        kneeMiddleRight.move(20)
        kneeMiddleLeft.move(20)
        animate(speed/2)
        
        kneeFrontLeft.move(50)
        kneeRearRight.move(50)
        animate(speed/2)
        
        hipFrontLeft.move(45)
        hipRearRight.move(45)
        animate(speed)
        
        kneeFrontLeft.move(20)
        kneeRearRight.move(20)
        animate(speed/2)
        
        kneeFrontRight.move(50)
        kneeRearLeft.move(50)
        animate(speed/2)
        
        hipFrontRight.move(45)
        hipRearLeft.move(45)
        animate(speed)
        
        kneeFrontRight.move(20)
        kneeRearLeft.move(20)
        animate(speed/2)

#--------------------------------------------------------------
def VR612_walkbackward(steps, speed):
    kneeFrontLeft.move(50)
    kneeRearLeft.move(50)
    hipFrontLeft.move(15)
    hipFrontRight.move(75)
    
    hipFrontLeft.move(80)
    hipRearLeft.move(5)
    hipMiddleRight.move(115)
    animate(speed)
    
    for i in range(0, steps): 
        kneeFrontLeft.move(10)
        kneeRearLeft.move(10)
        kneeMiddleRight.move(10)
        animate(speed)
        
        kneeFrontRight.move(50)
        kneeRearRight.move(50)
        kneeMiddleLeft.move(50)
        animate(speed)
        
        kneeFrontLeft.move(20)
        kneeRearLeft.move(20)
        kneeMiddleRight.move(20)
        hipFrontLeft.move(45)
        hipRearLeft.move(45)
        hipMiddleRight.move(90)
        hipFrontRight.move(80)
        hipRearRight.move(5)
        hipMiddleLeft.move(115)
        animate(speed)
        
        kneeFrontRight.move(10)
        kneeRearRight.move(10)
        kneeMiddleLeft.move(10)
        animate(speed)
        
        kneeFrontLeft.move(50)
        kneeRearLeft.move(50)
        kneeMiddleRight.move(50)
        animate(speed)
        
        kneeFrontRight.move(20)
        kneeRearRight.move(20)
        kneeMiddleLeft.move(20)
        hipFrontRight.move(45)
        hipRearRight.move(45)
        hipMiddleLeft.move(90)
        hipFrontLeft.move(80)
        hipRearLeft.move(5)
        hipMiddleRight.move(115)
        animate(speed)
    
    kneeFrontLeft.move(10)
    kneeRearLeft.move(10)
    kneeMiddleRight.move(10)
    animate(speed)
    
    kneeFrontRight.move(50)
    kneeRearRight.move(50)
    kneeMiddleLeft.move(50)
    animate(speed)
    
    hipFrontLeft.move(45)
    hipRearLeft.move(45)
    hipMiddleRight.move(90)
    animate(speed)
    
    kneeFrontRight.move(20)
    kneeRearRight.move(20)
    kneeMiddleLeft.move(20)
    kneeFrontLeft.move(20)
    kneeRearLeft.move(20)
    kneeMiddleRight.move(20)
    animate(speed)

#--------------------------------------------------------------
def VR612_walkforward(steps, speed):
    kneeRearLeft.move(50)
    kneeFrontLeft.move(50)
    kneeMiddleRight.move(50)
    animate(speed)
    
    hipRearLeft.move(80)
    hipFrontLeft.move(5)
    hipMiddleRight.move(65)
    animate(speed)
    
    for i in range(0, steps): 
        kneeRearLeft.move(10)
        kneeFrontLeft.move(10)
        kneeMiddleRight.move(10)
        animate(speed)
        
        kneeRearRight.move(50)
        kneeFrontRight.move(50)
        kneeMiddleLeft.move(50)
        animate(speed)
        
        kneeRearLeft.move(20)
        kneeFrontLeft.move(20)
        kneeMiddleRight.move(20)
        hipRearLeft.move(45)
        hipFrontLeft.move(45)
        hipMiddleRight.move(90)
        hipRearRight.move(80)
        hipFrontRight.move(5)
        hipMiddleLeft.move(65)
        animate(speed)
        
        kneeRearRight.move(10)
        kneeFrontRight.move(10)
        kneeMiddleLeft.move(10)
        animate(speed)
        
        kneeRearLeft.move(50)
        kneeFrontLeft.move(50)
        kneeMiddleRight.move(50)
        animate(speed)
        
        kneeRearRight.move(20)
        kneeFrontRight.move(20)
        kneeMiddleLeft.move(20)
        hipRearRight.move(45)
        hipFrontRight.move(45)
        hipMiddleLeft.move(90)
        hipRearLeft.move(80)
        hipFrontLeft.move(5)
        hipMiddleRight.move(65)
        animate(speed)
    
    kneeRearLeft.move(10)
    kneeFrontLeft.move(10)
    kneeMiddleRight.move(10)
    animate(speed)
    
    kneeRearRight.move(50)
    kneeFrontRight.move(50)
    kneeMiddleLeft.move(50)
    animate(speed)
    
    hipRearLeft.move(45)
    hipFrontLeft.move(45)
    hipMiddleRight.move(90)
    animate(speed)
    
    kneeRearRight.move(20)
    kneeFrontRight.move(20)
    kneeMiddleLeft.move(20)
    kneeRearLeft.move(20)
    kneeFrontLeft.move(20)
    kneeMiddleRight.move(20)
    animate(speed)

#--------------------------------------------------------------
def VR612_leanforward(speed):
    kneeFrontLeft.move(90)
    kneeFrontRight.move(90)
    kneeMiddleRight.move(50)
    kneeMiddleLeft.move(50)
    animate(speed)
    
    time.sleep(speed/2)
    
    kneeFrontLeft.move(20)
    kneeFrontRight.move(20)
    kneeMiddleRight.move(20)
    kneeMiddleLeft.move(20)
    
    animate(speed)

#--------------------------------------------------------------
def VR612_leanbackward(speed):
    kneeRearLeft.move(90)
    kneeRearRight.move(90)
    kneeMiddleRight.move(50)
    kneeMiddleLeft.move(50)
    animate(speed)
    
    time.sleep(speed/2)
    
    kneeRearLeft.move(20)
    kneeRearRight.move(20)
    kneeMiddleRight.move(20)
    kneeMiddleLeft.move(20)
    
    animate(speed)

#--------------------------------------------------------------
def VR612_leanright(speed):
    kneeRearRight.move(10)
    kneeFrontRight.move(10)
    kneeMiddleRight.move(0)
    kneeRearLeft.move(90)
    kneeFrontLeft.move(90)
    kneeMiddleLeft.move(90)
    animate(speed)
    
    time.sleep(speed/2)
    
    kneeRearRight.move(20)
    kneeFrontRight.move(20)
    kneeMiddleRight.move(20)
    kneeRearLeft.move(20)
    kneeFrontLeft.move(20)
    kneeMiddleLeft.move(20)
    
    animate(speed)

#--------------------------------------------------------------
def VR612_leanleft(speed):
    kneeRearRight.move(90)
    kneeFrontRight.move(90)
    kneeMiddleRight.move(90)
    kneeRearLeft.move(10)
    kneeFrontLeft.move(10)
    kneeMiddleLeft.move(0)
    animate(speed)
    
    time.sleep(speed/2)
    
    kneeRearRight.move(20)
    kneeFrontRight.move(20)
    kneeMiddleRight.move(20)
    kneeRearLeft.move(20)
    kneeFrontLeft.move(20)
    kneeMiddleLeft.move(20)
    
    animate(speed)

#--------------------------------------------------------------
def VR612_lookleft(speed):
    hipRearLeft.move(80)
    hipRearRight.move(10)
    hipFrontLeft.move(10)
    hipFrontRight.move(80)
    hipMiddleRight.move(125)
    hipMiddleLeft.move(65)
    animate(speed)
    
    time.sleep(speed/2)
    
    hipRearRight.move(45)
    hipRearLeft.move(45)
    hipFrontRight.move(45)
    hipFrontLeft.move(45)
    hipMiddleRight.move(90)
    hipMiddleLeft.move(90)
    animate(speed)

#--------------------------------------------------------------
def VR612_lookright(speed):
    hipRearRight.move(80)
    hipRearLeft.move(10)
    hipFrontRight.move(10)
    hipFrontLeft.move(80)
    hipMiddleRight.move(65)
    hipMiddleLeft.move(125)    
    animate(speed)
    
    time.sleep(speed/2)
    
    hipRearRight.move(45)
    hipRearLeft.move(45)
    hipFrontRight.move(45)
    hipFrontLeft.move(45)
    hipMiddleRight.move(90)
    hipMiddleLeft.move(90)
    animate(speed)

#--------------------------------------------------------------
# Initialise the spider robot:
VR612_reset_spider()

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
        VR612_leanforward(random.uniform(.001, .0255))
    elif action == 1:
        VR612_leanbackward(random.uniform(.001, .0255))
    elif action == 2:
        VR612_leanleft(random.uniform(.001, .0255))
    elif action == 3:
        VR612_leanright(random.uniform(.001, .0255))
    elif action == 4:
        VR612_lookleft(random.uniform(.001, .0255))
    elif action == 5:
        VR612_lookright(random.uniform(.001, .0255))
    elif action == 6:
        VR612_turnleft(random.randint(1, 5), random.uniform(.001, .0255))
    elif action == 7:
        VR612_turnright(random.randint(1, 5), random.uniform(.001, .0255))
    elif action == 8:
        VR612_walkforward(random.randint(2, 10), random.uniform(.001, .015))
    elif action == 9:
        VR612_walkbackward(random.randint(2, 10), random.uniform(.001, .015))
    elif action == 10:
        VR612_walkleft(random.randint(2, 10), random.uniform(.001, .015))
    elif action == 11:
        VR612_walkright(random.randint(2, 10), random.uniform(.001, .015))
    elif action == 12:
        VR612_scared(random.randint(2, 10), random.uniform(.0005, .003))
    elif action == 13:
        chirp(random.randint(1, 30), random.uniform(.0001, .0255))
    elif action == 14:
        VR612_wavefrontright(random.randint(1, 5), random.uniform(.0025, .01))
    elif action == 15:
        VR612_wavefrontleft(random.randint(1, 5), random.uniform(.0025, .01))
    elif action == 16:
        VR612_waverearright(random.randint(1, 5), random.uniform(.0025, .01))
    elif action == 17:
        VR612_waverearleft(random.randint(1, 5), random.uniform(.0025, .01))
