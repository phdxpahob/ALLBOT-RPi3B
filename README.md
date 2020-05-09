# ALLBOT-RPi3B
A set of python scripts for the [Velleman](https://manuals.velleman.eu/category.php?id=85) Robotics [ALLBOTs](https://manuals.velleman.eu/article.php?id=394). Work derived from the [original source code](https://github.com/Velleman/ALLBOT-lib/) for Arduino, ported to python.

## Hardware requirements:
Tested on Raspberry Pi 3B(+), using the Adafruit 16-Channel 12-bit PWM/Servo Driver with I2C interface using the [PCA9685](https://www.nxp.com/products/power-management/lighting-driver-and-controller-ics/ic-led-controllers/16-channel-12-bit-pwm-fm-plus-ic-bus-led-controller:PCA9685). Could be ported on a custom PCA9685 board.

## Software requirements:
The scripts require the [Adafruit Python PCA9685 library](https://github.com/adafruit/Adafruit_Python_PCA9685). 

## Known issuess
~~Currently there is no way to control the movement speed of the legs.~~ Added new class `WBServo` and `animate()` function, that allows code to be written the same way as using the Arduino ALLBOT-lib. Still holds that depending on the configuration, the movement angles should be corrected. This is now made simpler, because it could be set if the servo is inverted (flipped), and offset angle if the displacement is small. For bigger displacements mechanical tuning is required. Code cleanup and formatting contributions are still welcome!
