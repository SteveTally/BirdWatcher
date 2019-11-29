
#Test of varying resolution images#

scene_number = 3

from PIL import Image
import os

from aiy.vision.inference import ImageInference
from aiy.vision.models import inaturalist_classification


images_to_test = os.listdir("scene"+str(scene_number))

result_file = open('scene_'+str(scene_number)+'_res_test.txt','w+')

for image_name in images_to_test:
    with ImageInference(inaturalist_classification.model(inaturalist_classification.BIRDS)) as inference:
        image = Image.open('scene'+str(scene_number)+'/'+image_name)
        print(image_name)
        result = inference.run(image)
        classes = inaturalist_classification.get_classes(result,top_k=5,threshold=0.0)

        for i, (label, score) in enumerate(classes):
            print('Test: %s Result %d: %s (prob=%f)' % (image_name, i, label, score))
            result_file.write('Test: %s Result %d: %s (prob=%f)\n' % (image_name, i, label, score))



