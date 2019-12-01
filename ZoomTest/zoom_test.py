

#import argparse
#import contextlib

from aiy.vision.inference import CameraInference
#from aiy.vision.models import image_classification
from aiy.vision.models import inaturalist_classification
from picamera import PiCamera
#import datetime
import os.path
from os import path
import time

# Zoom Settings to Test
zoom_settings_list = [(0.5,0.5,0.25,0.25),(0.5,0,0.25,0.25)]


result_file = open('zoom_test.txt','w+')

#Initialize Camera
camera = PiCamera(sensor_mode=3, resolution = (700, 700))
camera.start_preview()
time.sleep(5)

# Set up inference
inference = CameraInference(inaturalist_classification.model(inaturalist_classification.BIRDS))

setting_number = 1
for zoom_setting in zoom_settings_list:
         camera.zoom = (zoom_setting) #set zoom and AOI
         time.sleep(1)
         result = inference.run() #run inference
         classes = inaturalist_classification.get_classes(result, top_k=10, threshold = 0)

         for i, (label, score) in enumerate(classes):
            print('%d %s - %d: %s (prob=%f)' % (setting_number,str(zoom_setting), i, label, score))
            result_file.write('%d %s - %d: %s (prob=%f)\n' % (setting_number,str(zoom_setting), i, label, score))
            camera.capture(str(setting_number)+'.jpg')
            setting_number = setting_number+1

result_file.close() # close the output file
