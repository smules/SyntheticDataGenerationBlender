import os
import sys
generate_images = os.path.dirname(os.path.realpath(__file__)) + '/'
sys.path.append(generate_images)
sys.path.append('/usr/local/lib/python3.5/dist-packages')
from utils.upper_level_coordinator import Coordinator


model_location = '/home/blender/Desktop/Test/Parts sample/'#where the models we want to render are
model_range = [-.1,.1]
save_location = '/home/blender/Desktop/Test/Image save/'#were you want the examples to be saved
#maybe add background images. Will need those
number_of_models = len(os.listdir(model_location))
model_names = os.listdir(model_location)#reads "model_location" to name all of the folders in save_location
print(model_names[3])
examples_quantity = 10
examples_res = (128,128)
cam_zoom = [-.3,.3]
num_lights = 3
background_save_path = '/home/blender/Desktop/Test/Background save/'#path to were to save blank backgrounds

start = Coordinator(model_location, number_of_models, save_location, model_names, examples_quantity, examples_res, cam_zoom, num_lights,
                    model_range, background_save_path)
start.rendering()
