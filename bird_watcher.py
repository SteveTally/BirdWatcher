#### Bird Watcher ####
# 


#import contextlib

from aiy.vision.inference import ImageInference
#from aiy.vision.models import image_classification
from aiy.vision.models import inaturalist_classification
from picamera import PiCamera
from datetime import datetime
#import os.path
#from os import path
#import time
from PIL import Image, ImageOps
import io
from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTClient
#from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTClient



class BirdCamera():
    def __init__(self,regions_of_interest):
        self.regions_of_interest = regions_of_interest

        print("starting camera...")
        # Set Sensor Mode
        self.camera = PiCamera(sensor_mode=3)
        self.camera.resolution = (1640,1232)

        #### Compensate for Snowy Background ####
        self.camera.meter_mode = 'backlit'
        self.camera.brightness = 35
        self.camera.exposure_compensation = 8

        # Start Camear #
        self.camera.start_preview()

    def capture(self):
        # captture image from camera
        self.image_stream = io.BytesIO() # start a new stream object
        self.camera.capture(self.image_stream, 'jpeg') # capture the image to the stream
        self.image_stream.seek(0) # move back to the start of the image stream
        self.image = Image.open(self.image_stream) # open the image stream as a PIL opbject
        
        self.image_dict = self.regions_of_interest.copy()
        for region_name in self.regions_of_interest:
            self.image_dict[region_name] = (self.image.crop(self.regions_of_interest[region_name]).copy())
        return self.image_dict
    def stop(self):
        self.camera.stop_preview()




class AWSDataLogger():

    def __init__(self, topic):
        self.host = "a2g5pwtppcagwt-ats.iot.us-east-1.amazonaws.com"
        #certPath = "/home/pi/BirdWatcher/AWSCertificates/"
        self.clientId = "RaspberryPi_BirdWatcher"
        self.topic = topic
        # Initialize Client
        self.AWSClient = None
        self.AWSClient = AWSIoTMQTTClient(self.clientId)
        self.AWSClient.configureEndpoint(self.host, 8883)
        self.AWSClient.configureCredentials("/home/pi/cert/CA1.pem", "/home/pi/cert/8fff3b9b49-private.pem.key", "/home/pi/cert/8fff3b9b49-certificate.pem.crt")
    
        # Configure Client
        self.AWSClient.configureAutoReconnectBackoffTime(1, 32, 20)
        self.AWSClient.configureOfflinePublishQueueing(-1)  # Infinite offline Publish queueing
        self.AWSClient.configureDrainingFrequency(2)  # Draining: 2 Hz
        self.AWSClient.configureConnectDisconnectTimeout(10)  # 10 sec
        self.AWSClient.configureMQTTOperationTimeout(5)  # 5 sec
        self.AWSClient.connect()
        
    def publish(self, image_name,species,probability,image_region):
        now = datetime.utcnow()
        now_str = now.strftime('%Y-%m-%d %H:%M:%SZ') 
        
        self.payload = '{ "timestamp": "' + now_str + '","species": "' + species + '","probability": '+ str(round(probability,2)) + ',"image_region": "'+image_region+  '","image_name": "'+ image_name+'" }'
        self.AWSClient.publish(self.topic, self.payload, 0)
        

class BirdInference():
    def __init__(self):
        print("starting inference..")
        self.inference = ImageInference(inaturalist_classification.model(inaturalist_classification.BIRDS))
    def run(self, image):
        self.result = self.inference.run(image)
        self.bird_class = inaturalist_classification.get_classes(self.result, top_k=1, threshold = 0.8)
        if len(self.bird_class) == 0: # if nothing is found, return none
            return None
        elif self.bird_class[0][0] == 'background':# if background is found, return none
            return None
        else: # If a bird clas is returned, flip the image, run again and ensure same class is returned
            self.result_2 = self.inference.run(ImageOps.mirror(image))
            self.bird_class_2 = inaturalist_classification.get_classes(self.result_2, top_k=1, threshold = 0.8)
            if len(self.bird_class_2) == 0:
                return None
            else:
                if self.bird_class_2[0][0] == self.bird_class[0][0]:
                    return self.bird_class[0]
                else:
                    return None
    
        #TODO: double inference
        #Remobe background and only return the top class
        

def main():

    # set up camera
    camera = BirdCamera(regions_of_interest = {'ll': (389,710,736,920), 'ur': (660,580,969,810), 'lr': (640,800,994,1060)})
    # initialize data logger
    data_logger = AWSDataLogger(topic = "bird_sighting")
    # load inference engine
    bird_inference = BirdInference()
    
    # loop durring day hours
    i = 0
    while datetime.now().hour <= 20:
        # check to see if time is between 7 AM and 6 PM
            
            image_dict = camera.capture() # capture image
            print(i, end='\r')
            for region, image in  image_dict.items():
                result = bird_inference.run(image)
                
                if result:
                    image_name = result[0]+str(datetime.now())+'.jpg'
                    data_logger.publish(image_name = image_name,species = result[0],probability = result[1],image_region = region)
                    image.save('Output/Images/'+image_name)
                    print(result[0])
            i = i +1                    

if __name__ == "__main__":
    main()