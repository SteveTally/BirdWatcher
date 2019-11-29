# Capture a still image from the camera
from picamera import PiCamera
import time

camera =  PiCamera(sensor_mode=3)
camera.resolution = (1000, 2464)
camera.zoom = (0.1,0.1,0.8,0.8)
camera.start_preview()
time.sleep(5)
camera.capture('Output/test_image_zoom.jpg')
camera.stop_preview()
