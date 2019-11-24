# Capture a still image from the camera
from picamera import PiCamera
import time

camera =  PiCamera(sensor_mode=4)
camera.resolution = (1640, 1232)
camera.start_preview()
time.sleep(5)
camera.capture('Output/test_image.jpg')
camera.stop_preview()
