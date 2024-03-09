import datetime
import sys
from gpiozero import LED
from picamera import PiCamera
from time import sleep
from fractions import Fraction

"""
Run file with python flor_image_emiss.py LED_WV

Potential Values of LED_WV: 490 or 770 (refers to potential excitation wavelengths used, corresponding to fluorophore)

"""

# Creating Unique filename based on the time the image was captured
cur_time = datetime.datetime.now()
cur_time_str = cur_time.strftime("%m%d%H%M%S")

# Initialize Camera with proper settings
camera = PiCamera(framerate = Fraction(1,6))
camera.resolution = (1280,768) # (1280,768) Max on Laptop as of 3/13/2022
camera.shutter_speed = 400_000 # max of 6 seconds of exposure (manipulate first & in microseconds);
camera.iso = 100  # Works with 100, better to manipulate 2nd since it determines light sensitivity, amplifies image signal
camera.rotation = 180
sleep(30)
camera.exposure_mode = 'off'

# Initializing Specific Excitation LED
if (sys.argv[1] == 770):
    led_ex = LED(3) # 770 nm LED (LICOR)
    led_name = "_770"
else:
    led_ex = LED(18) # 490 nm LED (FAM)
    led_name = "_490"

# Define String for Final Img Filename
file_str = cur_time_str + led_name

# Code for Excitation & Image Capture of Fluorophore Emission
camera.start_preview()
led_ex.on()
camera.capture('/home/pi/Pictures/%s.png' % file_str)
camera.stop_preview()
led_ex.off()
camera.close()
