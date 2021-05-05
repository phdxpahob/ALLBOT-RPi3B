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

def initPWM(addr=0x40, bus=1, smin=111, smax=489, freq=50):
    global pwm
    global servo_min, servo_max
    # Initialise the PCA9685
    pwm = Adafruit_PCA9685.PCA9685(address=addr, busnum=bus)
    # Set PWM frequency. 
    # You can use 60Hz, but you have to change servo _min & _max.
    pwm.set_pwm_freq(freq)
    # Configure min and max servo pulse lengths
    # These values are based on the assumptions that pwm frequency is 50 Hz.
    # If you intend to use 60Hz uncomment the other values instead.
    servo_min = smin #150  
    servo_max = smax #600  


def resetPWM(addr=0x40, bus=1):
    global pwm
    pwm = Adafruit_PCA9685.PCA9685()

def set_servo_angle(degg):
    """ 
    Helper function to calculate the servo pulse value for pwm.set_pwm()
    """
    global servo_min, servo_max
    if degg > 180:
        degg = 180
    elif degg < 0:
        degg = 0
    servopuls = int(servo_min + (servo_max-servo_min)/180 * degg)
    return servopuls

class WBServo:
    """
    Walking robot servo control class, based on ALLBOT arduino/cpp class
    """
    
    def __init__(self, pin, flipped, offset, angle):
        global pwm
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
    It compares if angle & to_angle are equal and if not, then they are 
    moved with a single degree per time delay, until to_angle and angle 
    are equal.
    """
    global pwm
    not_done = True
    while not_done:
        not_done = False
        for i in servos():
            if i.angle != i.to_angle:
                i.angle += 1 if i.angle<i.to_angle else -1
                not_done = True
                pwm.set_pwm(i.pin, 0, set_servo_angle(i.angle))
        time.sleep(speedms)

def servos():
    """
    This is a name list, that is required for animate() to function.
    """
    global hipFrontLeft
    global kneeFrontLeft
    global hipFrontRight
    global kneeFrontRight
    global hipRearLeft
    global kneeRearLeft
    global hipRearRight
    global kneeRearRight
    
    yield hipFrontLeft
    yield hipFrontRight
    yield hipRearLeft
    yield hipRearRight
    yield kneeFrontLeft
    yield kneeFrontRight
    yield kneeRearLeft
    yield kneeRearRight

#<------------ problem
# Here are initialized all the joints, Arduino ALLBOT-lib style.
# NAME = WBServo(pin, flipped, offset, init_angle)
def configurejoints():
    """
    This function defines/configures the servos.
    
    It has inherent downside, that programatically the objects cannot 
    be modified. The only way is to access the class object properties
    is from outside, which is against the recommendations.
    """
    global hipFrontLeft
    global kneeFrontLeft
    global hipFrontRight
    global kneeFrontRight
    global hipRearLeft
    global kneeRearLeft
    global hipRearRight
    global kneeRearRight
    
    hipFrontLeft = WBServo(8, False, 0, 45)
    kneeFrontLeft = WBServo(9, False, 0, 45)
    hipFrontRight = WBServo(12, True, 0, 45)
    kneeFrontRight = WBServo(13, False, 0, 45)
    hipRearLeft = WBServo(4, True, 0, 45)
    kneeRearLeft = WBServo(5, True, 0, 45)
    hipRearRight = WBServo(0, False, 0, 45)
    kneeRearRight = WBServo(1, True, 0, 45)

def reset_spider():
    """
    Stand-still position of the ALLBOT VR408
    """
    global hipFrontLeft
    global kneeFrontLeft
    global hipFrontRight
    global kneeFrontRight
    global hipRearLeft
    global kneeRearLeft
    global hipRearRight
    global kneeRearRight
    
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
def waverearleft(waves, speed):
    global hipRearLeft
    global kneeRearLeft
    
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
def waverearright(waves, speed):
    global hipRearRight
    global kneeRearRight
    
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
def wavefrontright(waves, speed):
    global hipFrontRight
    global kneeFrontRight
    
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
def wavefrontleft(waves, speed):
    global hipFrontLeft
    global kneeFrontLeft
    
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
def scared(shakes, beeps):
    global hipFrontLeft
    global kneeFrontLeft
    global hipFrontRight
    global kneeFrontRight
    global hipRearLeft
    global kneeRearLeft
    global hipRearRight
    global kneeRearRight
    
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
def leanbackward(speed):
    global kneeRearLeft
    global kneeRearRight
    
    kneeRearLeft.move(90)
    kneeRearRight.move(90)
    animate(speed)
    
    time.sleep(speed/2)
    
    kneeRearLeft.move(45)
    kneeRearRight.move(45)
    animate(speed)

#--------------------------------------------------------------
def leanleft(speed):
    global kneeFrontLeft
    global kneeRearLeft
    
    kneeFrontLeft.move(90)
    kneeRearLeft.move(90)
    animate(speed)
    
    time.sleep(speed/2)
    
    kneeFrontLeft.move(45)
    kneeRearLeft.move(45)
    animate(speed)

#--------------------------------------------------------------
def leanright(speed):
    global kneeFrontRight
    global kneeRearRight
    
    kneeFrontRight.move(90)
    kneeRearRight.move(90)
    animate(speed)
    
    time.sleep(speed/2)
    
    kneeFrontRight.move(45)
    kneeRearRight.move(45)
    animate(speed)

#--------------------------------------------------------------
def leanforward(speed):
    global kneeFrontLeft
    global kneeFrontRight
    
    kneeFrontLeft.move(90)
    kneeFrontRight.move(90)
    animate(speed)
    
    time.sleep(speed/2)
    
    kneeFrontLeft.move(45)
    kneeFrontRight.move(45)
    animate(speed)

#--------------------------------------------------------------
def lookleft(speed):
    global hipFrontLeft
    global hipFrontRight
    global hipRearLeft
    global hipRearRight
    
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
def lookright(speed):
    global hipFrontLeft
    global hipFrontRight
    global hipRearLeft
    global hipRearRight
    
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
def walkforward(steps, speed):
    global hipFrontLeft
    global kneeFrontLeft
    global hipFrontRight
    global kneeFrontRight
    global hipRearLeft
    global kneeRearLeft
    global hipRearRight
    global kneeRearRight
    
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
def walkbackward(steps, speed):
    global hipFrontLeft
    global kneeFrontLeft
    global hipFrontRight
    global kneeFrontRight
    global hipRearLeft
    global kneeRearLeft
    global hipRearRight
    global kneeRearRight
    
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
def walkright(steps, speed):
    global hipFrontLeft
    global kneeFrontLeft
    global hipFrontRight
    global kneeFrontRight
    global hipRearLeft
    global kneeRearLeft
    global hipRearRight
    global kneeRearRight
    
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
def walkleft(steps, speed):
    global hipFrontLeft
    global kneeFrontLeft
    global hipFrontRight
    global kneeFrontRight
    global hipRearLeft
    global kneeRearLeft
    global hipRearRight
    global kneeRearRight
    
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
def turnleft(steps, speed):
    global hipFrontLeft
    global kneeFrontLeft
    global hipFrontRight
    global kneeFrontRight
    global hipRearLeft
    global kneeRearLeft
    global hipRearRight
    global kneeRearRight
    
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
def turnright(steps, speed):
    global hipFrontLeft
    global kneeFrontLeft
    global hipFrontRight
    global kneeFrontRight
    global hipRearLeft
    global kneeRearLeft
    global hipRearRight
    global kneeRearRight
    
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

#==============================================================

def ProductDemo():
    """
    This function does a random action with random values.
    Can be invoked for testing purposes, or placed in a loop to 
    demonstrate the capabilities of the robot.
    """
    action = random.randint(0, 17)
    if action == 0:
        leanforward(random.uniform(.001, .0255))
    elif action == 1:
        leanbackward(random.uniform(.001, .0255))
    elif action == 2:
        leanleft(random.uniform(.001, .0255))
    elif action == 3:
        leanright(random.uniform(.001, .0255))
    elif action == 4:
        lookleft(random.uniform(.001, .0255))
    elif action == 5:
        lookright(random.uniform(.001, .0255))
    elif action == 6:
        turnleft(random.randint(1, 5), random.uniform(.001, .0255))
    elif action == 7:
        turnright(random.randint(1, 5), random.uniform(.001, .0255))
    elif action == 8:
        walkforward(random.randint(2, 10), random.uniform(.001, .015))
    elif action == 9:
        walkbackward(random.randint(2, 10), random.uniform(.001, .015))
    elif action == 10:
        walkleft(random.randint(2, 10), random.uniform(.001, .015))
    elif action == 11:
        walkright(random.randint(2, 10), random.uniform(.001, .015))
    elif action == 12:
        scared(random.randint(2, 10), random.uniform(.0005, .003))
    elif action == 13:
        chirp(random.randint(1, 30), random.uniform(.0001, .0255))
    elif action == 14:
        wavefrontright(random.randint(1, 5), random.uniform(.0025, .01))
    elif action == 15:
        wavefrontleft(random.randint(1, 5), random.uniform(.0025, .01))
    elif action == 16:
        waverearright(random.randint(1, 5), random.uniform(.0025, .01))
    elif action == 17:
        waverearleft(random.randint(1, 5), random.uniform(.0025, .01))
        # return string with the action, example: "Step Forward. Speed {} s".format(self.speedSlider.value()/1000)

def ProductDemoContinuous():
    """
    This function places ProductDemo() in a loop until the user exits
    with keyboard input. Default entry point if script is invoked
    standalone.
    """
    print("VR408 Product demo, press Ctrl+C to stop...") # The only way to exit...
    
    # Random action infinite loop:
    while True:
        try:    
            time.sleep(random.uniform(0.001, 0.02));
            ProductDemo()
        
        except KeyboardInterrupt:
            print("Exiting...")
            reset_spider()
            break


#If executed as plain script from the CLI, do a product demo. 
#The functions can be used in other scripts if imported as a module.
#This way the code below will not be executed. However the init 
#sequence below should be preserved in order to "start" the robot.
if __name__ == "__main__":
    # Initialise the spider robot:
    initPWM()
    configurejoints()
    reset_spider()
    
    # Chirp for ready:
    chirp(1, 50)
    chirp(1, 255)
    chirp(3, 0)
    
    time.sleep(2) # 2 seconds time delay before random actions
    
    ProductDemoContinuous()
    resetPWM()
