# ALLBOT-RPi3B Example scripts
A set of python scripts for the [Velleman](https://manuals.velleman.eu/category.php?id=85) Robotics [ALLBOTs](https://manuals.velleman.eu/article.php?id=394). Work derived from the [original source code](https://github.com/Velleman/ALLBOT-lib/) for Arduino, ported to python.

## Hardware requirements:
Tested on Raspberry Pi 3B(+), using the Adafruit 16-Channel 12-bit PWM/Servo Driver with I2C interface using the [PCA9685](https://www.nxp.com/products/power-management/lighting-driver-and-controller-ics/ic-led-controllers/16-channel-12-bit-pwm-fm-plus-ic-bus-led-controller:PCA9685). For example:
- [Adafruit 16-Channel PWM/Servo HAT & Bonnet for Raspberry Pi](https://learn.adafruit.com/adafruit-16-channel-pwm-servo-hat-for-raspberry-pi)
- [Adafruit PCA9685 16-Channel Servo Driver](https://learn.adafruit.com/16-channel-pwm-servo-driver/overview)

Could be used also on other or even a custom PCA9685 board.
- [SparkFun Servo pHAT for Raspberry Pi](https://www.sparkfun.com/products/15316)

## Software requirements:
The scripts require the [Adafruit Python PCA9685 library](https://github.com/adafruit/Adafruit_Python_PCA9685). 

## Known issuess
- The original Velleman robots have a remote control module VR001 IR Transmitter, which is used to teleoperate the robot from smartphone, tablet etc. Since the RPi has wireless conectivities such as WiFi and Bluetooth, porting the section of the code, that handles this communication is not made. Instead the developer can use the routines along with scripts/code that handles this communication in desirable way -- wireless USB joystick, WiFi, Bluetooth, USB 3G module to name a few.
- ~~Currently there is no way to control the movement speed of the legs.~~ Added new class `WBServo` and `animate()` function, that allows code to be written the same way as using the Arduino ALLBOT-lib. Still holds that depending on the configuration, the movement angles should be corrected. This is now made simpler, because it could be set if the servo is inverted (flipped), and offset angle if the displacement is small. For bigger displacements mechanical tuning is required. 
- Timing using `time.sleep` is not as precise as the Arduino `delay()`; also time constants should be lower to mimick the behaivior as in the original Arduino-controlled ALLBOTs. 
- Code cleanup and formatting contributions are still welcome!
