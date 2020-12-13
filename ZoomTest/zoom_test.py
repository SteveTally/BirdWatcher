#### AIY Vision Kit Zoom /AOI Test ####
# Test script to determine if camera digital zoom and croppint
# is performed before image goes to vision hat module
# or in software after it gets to the raspberry pi.  Having the
# ability to digitally zoom could substantially improve inference
# performance when a relatively small area of the frame could contain
# an object of interest.  This is the case with the birdfeeder app
# that I am currently working on.  I have some suspicion that the zoom
# operation is completed in software after it gets to the pi.

# To test this, the camera will be pointed at an image with
# different birds in three quadrants and blank quadrant
# the camera will iterate through four zoom / area of interest
# settings that isolate each quadrant of the image
# inference will be run and loogged and an image will be stored
# for each setting

# If the zoom is done on the camera module then the four zoom
# settings should have remarkably different inference results,
# otherwise I would expect them to be very similar.

from aiy.vision.inference import CameraInference
from aiy.vision.models import inaturalist_classification
from picamera import PiCamera
import os.path
from os import path
import time

# Zoom Settings to Test: Full fram, lower right, upper right, lower left, upper left
zoom_settings_list = [(0,0,1,1),(0.5,0.5,0.5,0.5),(0.5,0,0.5,0.5),(0,0.5,0.5,0.5),(0,0,0.5,0.5)]


result_file = open('zoom_test.txt','w+')

#Initialize Camera
print("starting camera...")
camera = PiCamera(sensor_mode=4)
camera.start_preview()
time.sleep(5)

# Set up inference
print("starting inference...")
inference = CameraInference(inaturalist_classification.model(inaturalist_classification.BIRDS))

setting_number = 1
for zoom_setting in zoom_settings_list:
        camera.zoom = (zoom_setting) #set zoom and AOI
        time.sleep(1)
        camera.capture(str(setting_number)+'.jpg')
        for result in inference.run(1): #run inference
            classes = inaturalist_classification.get_classes(result, top_k=10, threshold = 0)
            for i, (label, score) in enumerate(classes):
                print('%d %s - %d: %s (prob=%f)' % (setting_number,str(zoom_setting), i, label, score))
                result_file.write('%d %s - %d: %s (prob=%f)\n' % (setting_number,str(zoom_setting), i, label, score))
        setting_number = setting_number+1

result_file.close() # close the output file
inference.close()
