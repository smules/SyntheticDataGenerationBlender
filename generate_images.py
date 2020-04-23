import os
import sys
from .upper_level_coordinator import Coordinator


model_location = #where the models we want to render are
model_range = [-.1,.1]
save_location = #were you want the examples to be saved
#maybe add background images. Will need those
number_of_models = len(os.listdir(model_location))
model_names = []#reads "model_location" to name all of the folders in save_location
for x in range(0,number_of_models):
    model_names.append(os.listdir(model_location))#need to test. Populates for loop with the name of all the models
examples_quantity = 10
examples_res = (128,128)
cam_zoom = [-.3,.3]
num_lights = 3
background_save_path = #path to were to save blank backgrounds

start = Coordinator(model_location, number_of_models, save_location, model_names, examples_quantity, examples_res, cam_zoom, num_lights,
                    model_range)
start.rendering()
