
import unittest

from PIL import Image
from bird_watcher import BirdCamera
from bird_watcher import BirdInference
from bird_watcher import AWSDataLogger

class BirdWatcherTest(unittest.TestCase):
    
    def test_image_capture(self):
        # Create a BirdCamera object with set regions of interest
        camera = BirdCamera(regions_of_interest = {'ll': (389,710,736,920),
                                                   'ur': (660,580,969,810),
                                                   'lr': (640,800,994,1060)})
        image_dict = camera.capture() # trigger capture
        self.assertEqual(len(image_dict),3) # ensure three items were returned in the dictionary
        for region, image in  image_dict.items():
            self.assertIsInstance(image,Image.Image,"camera did not return a PIL image") # verify each image is a PIL image
            image.save('Output/UnitTest/Camera_Capture/'+region+'.jpg') # save image for inspection

    def test_inference(self):
        bird_inference = BirdInference()
        im1 = Image.open('Output/UnitTest/Image_Inference/None.jpg')
        result1 = bird_inference.run(im1)
        self.assertEqual(result1, None, "Blank inference test did not return none type")

        im2 = Image.open('Output/UnitTest/Image_Inference/Picoides pubescens (Downy Woodpecker).jpg')
        result2 = bird_inference.run(im2)
        self.assertEqual(result2[0],'Picoides pubescens (Downy Woodpecker)',"Woodpecker test image incorrectly classified")

    def test_aws_data_logger(self):
           data_logger = AWSDataLogger(topic = 'bird_watcher_test')
           data_logger.publish(image_name = "Picoides pubescens (Downy Woodpecker).jpg",species = "Picoides pubescens (Downy Woodpecker)",probability = 0.85,image_region = "ur")


if __name__ == '__main__':
    unittest.main()