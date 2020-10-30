import os
import sys
generate_images = os.path.dirname(os.path.realpath(__file__)) + '/'
sys.path.append(generate_images)
sys.path.append('/usr/local/lib/python3.5/dist-packages')
sys.path.insert(0, '/home/blender/Desktop/ImportLDraw-master/loadldraw/')
sys.path.append
#from utils.upper_level_coordinator import Coordinator
import random
import bpy
import numpy
import math
from mathutils import Vector
from numpy.random import uniform
from numpy.random import randint
import loadldraw


class Render():
    def __init__(self, model_location, save_location, number_of_models, model_names,
             examples_quantity, examples_res, num_lights):
        self.model_location =model_location
        self.save_location =save_location
        self.number_of_models = number_of_models
        self.model_names = model_names
        self.examples_quantity= examples_quantity
        self.examples_res = examples_res
        self.num_lights  =num_lights
        
        
    def set_render_properties():
        # Sets the Blender proterties like resolution
        #film_transparent removes a pink tint caused by the loadldraw library
        #color_mode = 'RGBA' includes alpha so the background can be transparant, outputs .png
        bpy.context.scene.render.resolution_x = 500
        bpy.context.scene.render.resolution_y = 500
        bpy.context.scene.render.resolution_percentage = 100
        bpy.context.scene.render.film_transparent = True
        bpy.context.scene.render.image_settings.color_mode = 'RGBA'

    def delete_scene():
        #Deletes the whole scene so a new one can be made
        bpy.ops.object.select_all(action='SELECT')
        bpy.ops.object.delete()

    def insert_camera():
        #Inserts a new camera, called when scene is being generated
        scene=bpy.context.scene
        cam=bpy.data.cameras.new('camera')
        cam.lens = 18
        cam_obj = bpy.data.objects.new('camera', cam)
        #randomizes the location of the camera
        cam_obj.location = (random.uniform(.5,1.5), random.uniform(-.5,-1.5), random.uniform(.5,1.5))
        #Points the camera to the middle
        cam_obj.rotation_euler = (1.11003293, 0,.81498132 )
        scene.collection.objects.link(cam_obj)

    def insert_model(model_location, pieces, model_names):
        #Loads a new model using the loadldraw library
        loadldraw.loadFromFile('test', model_location+model_names[pieces])
        bpy.data.objects['LegoGroundPlane'].location.z+=-1.0

    def lights(num_lights):
        #Inserts lights
        #Set number of lights; set to 3 for debug, but line directly below can be removed
        num_lights = 3
        bpy.ops.object.select_by_type(type='LIGHT')
        bpy.ops.object.delete()
        #Finds the amount of lights that are going to be used
        lights = random.randint(1, num_lights)
        #Makes new lights the randomized amount of time
        for num in range(0, lights):
            light_data = bpy.data.lights.new(name="light_"+str(num), type='POINT')
            light_data.energy = 30
            light_object = bpy.data.objects.new(name="light_"+str(num), object_data=light_data)
            bpy.context.collection.objects.link(light_object)
            bpy.context.view_layer.objects.active = light_object
            light_object.location = (random.uniform(-3.0,3.0), random.uniform(-3.0,3.0), random.uniform(0.0, 5.0))
            dg = bpy.context.evaluated_depsgraph_get() 
            dg.update()
    
    def rotate_piece(pieces, model_names):
        #Selects object and randomized its rotation
        bpy.data.objects['00000_'+model_names[pieces]].select_set(True)
        bpy.context.active_object.rotation_mode = 'XYZ'
        bpy.context.active_object.rotation_euler=(random.random()*math.radians(360), random.random()*math.radians(360), random.random()*math.radians(360))

    def render_image(filepath, name, camera_name='camera'):
        #Finally renders the image; not to be confused with def render(), which is main method
        objects = bpy.data.objects
        #Saves to filepath
        bpy.context.scene.render.filepath = filepath+name
        #Selects camera
        camera = objects[camera_name]
        bpy.context.scene.camera = camera
        bpy.ops.render.render(write_still=True)
    
    def render():
        #Coordinates the whole program, this is the main method once everything is importd
        Render.set_render_properties()
        for pieces in range(0, number_of_models):
            Render.delete_scene()
            Render.insert_camera()
            Render.insert_model(model_location, pieces, model_names)
            for ex in range(0, examples_quantity):
                Render.lights(num_lights)
                Render.rotate_piece(pieces, model_names)
                name=model_names[pieces]+'_'+str(ex)
                Render.render_image(save_location, name)



model_location = '/home/blender/Desktop/Test/Parts sample/'
save_location = '/home/blender/Desktop/Test/Image save/'
number_of_models = len(os.listdir(model_location))
model_names = os.listdir(model_location)
examples_quantity = 10
examples_res = (128,128)
num_lights = 3
Render(model_location, save_location, number_of_models, model_names,
            examples_quantity, examples_res, num_lights)
Render.render()

