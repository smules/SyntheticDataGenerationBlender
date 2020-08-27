import os
import sys
generate_images = os.path.dirname(os.path.realpath(__file__)) + '/'
sys.path.append(generate_images)
sys.path.append('/usr/local/lib/python3.5/dist-packages')
sys.path.insert(0, '/Users/default/Downloads/ImportLDraw-master/loadldraw')
sys.path.append
#from utils.upper_level_coordinator import Coordinator
import random
import bpy
import numpy
from mathutils import Vector
from numpy.random import uniform
from numpy.random import randint
import loadldraw


model_location = '/home/blender/Desktop/Test/Parts sample/'
save_location = '/home/blender/Desktop/Test/Image save/'
number_of_models = len(os.listdir(model_location))
model_names = os.listdir(model_location)
examples_quantity = 10
examples_res = (128,128)
num_lights = 3
self.render(self, model_location, save_location, number_of_models, model_names,
            examples_quantity, examples_res, num_lights)

class render(self, model_location, save_location, number_of_models, model_names,
             examples_quantity, examples_res, num_lights):
    self.set_render_properties(self)
    for pieces in range(0, number_of_models)
        self.delete_scene(self)
        self.insert_camera(self)
        self.insert_model(self, model_location, pieces, model_names)
        for ex in range(0, examples quantity)
            self.lights(self, num_lights)
            self.rotate_piece(self, piece, model_names)
            name=model_names[pieces]+'_'+str(ex)
            self.render_image(self, save_location, name)

class set_render_properties(self):
    bpy.context.scene.render.resolution_x = 500
    bpy.context.scene.render.resolution_y = 500
    bpy.context.scene.render.resolution_percentage = 100

class delete_scene(self):
    bpy.ops.object.select_all(action='SELECT')
    bpy.ops.objects.delete()
    #might need to make it so it only deletes the lego piece and lights but not the camera

class insert_camera(self)
    scene=bpy.context.scene
    cam=bpy.cameras.data.new('camera')
    cam.lens = 18
    cam_obj = bpy.data.objects.new('camera', cam)
    cam_obj.location = (7.35889, -6.92579, 4.95831)
    cam_obj.rotation_degree = (63.6, 0, 46.7)
    scene.collection.objects.link(cam_obj)

class insert_model(self, model_location, pieces, model_names)
    loadldraw.loadFromFile(model_location + model_names[pieces])
    #not figured out yet work in progress

class lights(self, num_lights):
    num_lights = 3
    bpy.ops.object.select_by_type(type='LIGHT')
    bpy.ops.object.delete()
    lights = random.randint(1, num_lights)
    for num in range(0, lights):
        light_data = bpy.data.lights.new(name="light_"+str(num), type='POINT')
        light_data.energy = 30
        light_object = bpy.data.objects.new(name="light_"+str(num), object_data=light_data)
        bpy.context.collection.objects.link(light_object)
        bpy.context.view_layer.objects.active = light_object
        light_object.location = (random.uniform(-3.0,3.0), random.uniform(-3.0,3.0), random.uniform(0.0, 5.0))
        dg = bpy.context.evaluated_depsgraph_get() 
        dg.update()

class rotate_piece(pieces, model_names):
    bpy.data.objects[model_names[pieces]].select_set(True)
    bpy.context.active_object.rotation_mode = 'XYZ'
    bpy.context.active_object.rotation_euler = (random.random()*360, random.random()*360, random.random()*360)

def render_image(filepath, name, camera_name='Camera'):
    objects = bpy.data.objects
    bpy.context.scene.render.filepath = filepath+name
    camera = objects[camera_name]
    bpy.context.scene.camera = camera
    bpy.ops.render.render(write_still=True)
