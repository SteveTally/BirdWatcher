# Capture a still image from the camera
from picamera import PiCamera
import time

camera =  PiCamera(sensor_mode=3)
camera.resolution = (1080, 1920)
camera.start_preview()
time.sleep(5)
camera.capture('Output/test_image.jpg')
camera.stop_preview()
