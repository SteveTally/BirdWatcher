
from PIL import Image
from picamera import PiCamera
from PIL import Image, ImageOps
import pickle

# Initialize Camera #
camera = PiCamera(sensor_mode=3)
camera.resolution = (1640,1232)

# Start Camear #
camera.start_preview()

# Capture Image #
image_stream = io.BytesIO() # start a new stream object
camera.capture(self.image_stream, 'jpeg') # capture the image to the stream
image_stream.seek(0) # move back to the start of the image stream
image = Image.open(self.image_stream) # open the image stream as a PIL opbject

# Save PIL Image as Pickle
pickle.dump(image, open( "Output/Calibration/calibration_image.p", "wb" ))