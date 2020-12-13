

from PIL import Image


from bird_watcher import BirdCamera
from bird_watcher import BirdInference
from bird_watcher import AWSDataLogger


#### Test Image Capture ####
print("testing_camera...")
camera = BirdCamera(regions_of_interest = {'ll': (389,710,736,920), 'ur': (660,580,969,810), 'lr': (640,800,994,1060)})
image_dict = camera.capture()
for region, image in  image_dict.items():
    print(region, image.size)
    image.save('Output/UnitTest/Camera_Capture/'+region+'.jpg')


#### Test Image Inference ####
print("testing_inference...")
bird_inference = BirdInference()
im1 = Image.open('Output/UnitTest/Image_Inference/None.jpg')
result = bird_inference.run(im1)

im2 = Image.open('Output/UnitTest/Image_Inference/Picoides pubescens (Downy Woodpecker).jpg')
result2 = bird_inference.run(im2)

#### Test Data Logging ####
print("testing AWS data logger...")
data_logger = AWSDataLogger(topic = 'bird_watcher_test')
data_logger.publish(image_name = "Picoides pubescens (Downy Woodpecker).jpg",species = "Picoides pubescens (Downy Woodpecker)",probability = 0.85,image_region = "ur")