#import glob
import random
import bpy
import numpy
from mathutils import Vector
from numpy.random import uniform
from numpy.random import randint
from PIL import Image

class Coordinator:
    def __init__(self, model_location, number_of_models, save_location, model_names, examples_quantity, examples_res, cam_zoom,
                 num_lights, model_range, background_save_path):
         #stuff to check if everything is in the right place
        self.model_location = model_location
        self.number_of_models = number_of_models
        self.save_location = save_location
        self.model_names = model_names
        self.examples_quantity = examples_quantity
        self.examples_res = examples_res
        self.num_lights = num_lights
        self.light_location_range = [-15 ,15]#range of light locations
        self.light_energy_range = [1,15]#range that light brightness can be
        self.light_type= 'POINT'#type of light used
        self.rotation_range= [0,360]# range of rotation of object
        self.translation_range= model_range
        self.zoom_range= cam_zoom
        self.background = 'plain'
        self.background_save_path = background_save_path
        
#high level stuff found image_classifer
    def rendering(self):
        #for loop to iterate through each piece
        self.set_render_properties()
        bpy.ops.object.select_all(action='DESELECT')
        bpy.data.objects['Cube'].select_set(True)
        bpy.ops.objects.delete()
        for piece in self.model_names:
            #for loop for the amount of samples per piece we want
            for amount in range(0, self.examples_quantity):
                obj = self.create_scene(self.model_location, piece)
                #box_coordinates = self.get_bounding_box(obj)
                box_coordinates = Vector((.001,.001,.001))
                image_name = self.make_image_name(self.model_names, amount, box_coordinates, piece)
                self.point_camera('Camera', 'mesh')
                self.render_image(image_name)
                self.delete_scene(self.save_location)

    def set_render_properties(self):
        #Sets the resolution of the images
        bpy.context.scene.render.resolution_x = 125 #can be changed
        bpy.context.scene.render.resolution_y = 125 #can be changed
        bpy.context.scene.render.resolution_percentage = 100 #can be changed

    def create_scene(self, model_location, model_names):
        #moves and rotates the object, zooms camera, and adds background
        obj = self.load_obj(model_location, model_names)
        self.change_lighting(self.num_lights, self.light_location_range, self.light_energy_range,self.light_type)
        if self.rotation_range is not None:
            rotation = uniform(self.rotation_range[0],self.rotation_range[1], size=3)
            self.rotate_object(obj, rotation.tolist())
        self.view_selected_object()
        #if self.translation_range is not None:
        #    translation = uniform(self.translation_range[0], self.translation_range[1], size=3)
        #    self.translate_object(obj, translation.tolist())
        #if self.zoom_range is not None:
        #    zoom = uniform(self.zoom_range)
        #    self.zoom_camera(zoom)
        if self.background == 'plain':
            RGB_values = randint(0,256,3).tolist()
            self.add_plain_background(RGB_values)
        else:
            image = random.choice(self.background_image_paths)
            self.add_random_patch_background(image)
        #self.change_color(obj)
        self.update_scene()
        return obj

#Start of blender import part of this
    def load_obj(self,model_location, model_names):
        #Brings in the object into blender
        bpy.ops.import_scene.obj(filepath=model_location + model_names)
        obj_object = bpy.context.selected_objects[0]
        #bpy.context.scene.object.active = obj_object
        #***
        bpy.ops.object.select_all(action='DESELECT')
        MESH_OBJ = [m for m in bpy.context.scene.objects if m.type == 'MESH']
        for OBJ in MESH_OBJ:
            OBJ.select_set(state=True)
            bpy.context.view_layer.objects.active = OBJ
        bpy.ops.object.join()
        #***
        bpy.ops.object.join()
        obj_object.name = 'mesh'
        location = self.get_object_lowest_point(obj_object)
        self.move_origin(location, axis='z')
        obj_object.location = (0., 0., 0.)
        print(obj_object)
        return obj_object

    def get_object_lowest_point(self, obj_object):
        #THINK ABOUT THIS
        matrix_w = obj_object.matrix_world
        vectors = [matrix_w @ vertex.co for vertex in obj_object.data.vertices]
        #return min(vectors, key=lambda item: item.z)
        return vectors

    def move_origin(self, location, axis):
        #THINK ABOUT THIS
        saved_location = bpy.context.scene.cursor.location.copy()
        if axis == 'z':
            location = saved_location.x, saved_location.y, saved_location.z
        bpy.context.scene.cursor.location = location
        bpy.ops.object.origin_set(type = 'ORIGIN_CURSOR')
        bpy.context.scene.cursor.location = saved_location

    def get_bounding_box(self, obj):
        #Get how large the brick is to make a bounding box
        scene = bpy.context.scene
        camera = bpy.data.objects['Camera']
        x_image_projections = []
        y_image_projections = []
        for obj_vertix in obj.data.vertices:
            vertix = obj.matrix * obj.vertix.co
            #print(normalized_image_corner.x)
            normalized_image_corner = self.to_camera_view(scene, camera, vertix)
            x_image_projections.append(normalized_image_corner.x)
            y_image_projections.append(normalized_image_corner.y)
        x_image_projections = numpy.asarray(x_image_projections)
        y_image_projections = numpy.asarray(y_image_projections)
        print(x_image_projections)
        x_min = numpy.min(x_image_projections)
        x_max = numpy.max(x_image_projections)
        y_min = 1 - numpy.min(y_image_projections)
        y_max = 1 - numpy.max(y_image_projections)
        coordinates = (x_min, y_min, x_max, y_max)
        coordinates = [self.clamp(coordinate) for coordinate in coordinates]
        return coordinates

    def to_camera_view(self, scene, obj, vertix):
        #Get how large the brick is to make a bounding box
        co_local = obj.matrix.normalized().inverted() * vertix
        z = -co_local.z
        camera = obj.data
        frame = [-v for v in camera.view_fram(scene=scene)[:3]]
        if camera.type != 'ORTHO':
            if z == 0.0:
                return Vector((0.5, 0.5, 0.0))
            else:
                frame = [(v / (v.z / z)) for v in frame]
        min_x, max_x = frame[1].x, frame[2].x
        min_y, max_y = frame[0].y, frame[1].y
        x = (co_local.x - min_x) / (max_x - min_x)
        y = (co_local.y - min_y) / (max_y - min_y)
        return Vector((x, y, z))

    def clamp(self, x, minimum=0., maximum=1.):
        #Really couldn't tell you
        return max(minimum, min(x, maximum))

    def make_image_name(self, model_names, amount, box_coordinates, piece):
        #Make the name for the image
        am = str(amount)
        print(isinstance(piece, str))
        base_name = (self.save_location + piece + '/' + piece
                     + '_'
                     + am
                     + '_')
        box_coordinates = ['{:.3f}'.format(x) for x in box_coordinates]
        box_coordinates = '_'.join(box_coordinates)
        image_name = base_name + box_coordinates
        return image_name

    def render_image(self, image_name, camera_name = 'Camera'):
        #Renders the final image
        objects = bpy.data.objects
        bpy.context.scene.render.filepath = self.save_location + image_name
        camera = objects[camera_name]
        bpy.context.scene.camera = camera
        bpy.ops.render.render(write_still=True)


    def delete_scene(self, save_location):
        #Delete scene after rendered
        for o in bpy.data.objects:
            if o.type == 'MESH' or o.type == 'LAMP':
                o.select_set(True)
            else:
                o.select_set(False)
        bpy.ops.object.delete()
        bpy.ops.wm.save_as_mainfile(filepath = save_location+'backup')
        bpy.ops.wm.open_mainfile(filepath = save_location+'backup')


    def change_lighting(self, num_lights, light_location_range, light_energy_range, light_type):
        #Changes the lighting position, intensity, and amount
        num_lamps = numpy.random.randint(1, num_lights + 1)
        for lamp_arg in range(num_lights):
            lamp = self.add_lamp('lamp_' + str(lamp_arg))
            print(numpy.random.uniform(-15,15,3))
            lamp.location = numpy.random.uniform(light_location_range[0], light_location_range[1], 3)
            lamp.data.energy = numpy.random.randint(light_energy_range[0], light_energy_range[1])
            lamp.data.type = light_type

    def add_lamp(self, name):
        #Adds lamp
        scene = bpy.context.scene
        lamp_data = bpy.data.lights.new(name=name, type=self.light_type)
        lamp=bpy.data.objects.new(name=name, object_data=lamp_data)
        scene.collection.objects.link(lamp)
        lamp.location = (0., 0., 0.)
        return lamp

    def rotate_object(self, obj, rotation):
        #Rotates the object
        angles = numpy.deg2rad(rotation).tolist()
        obj.delta_rotation_euler = angles

    def view_selected_object(self):
        #THINK ABOUT THIS
        bpy.ops.view3d.camera_to_view_selected()

    def translate_object(self, obj, translation):
        #Translates the brick
        obj.location = translation

    def zoom_camera(self, zoom):
        #Zooms camera randomly
        camera = self.get_camera()
        location = numpy.asarray(camera.location)
        direction = camera.matrix_world.to_quaternion() @ Vector((0.0, 0.0, -1.0))
        direction = numpy.asarray(direction)
        new_camera_location = location + (zoom[0]*direction)
        camera.location = new_camera_location.tolist()

    def add_plain_background(self, RGB_values, height=200, width=200):
        #Makes a background and applys it
        image_array = numpy.zeros(shape=(height, width, 3))
        image_array[:, :, 0].fill(RGB_values[0])
        image_array[:, :, 1].fill(RGB_values[1])
        image_array[:, :, 2].fill(RGB_values[2])
        pil_image = Image.fromarray(image_array.astype('uint8'))
        pil_image.save(self.background_save_path + 'plain_background.png')
        self.add_image_background(self.background_save_path + 'plain_background.png')

    def add_random_patch_background(self, image, box_size=200):
        #Gets a random part of background image and makes it background
        image = Image.open(image)
        height, width = image.size[0:2]
        if height <= box_size or width <= box_size:
            RGB_values = numpy.random.randint(0, 256, 3).tolist()
            self.add_plain_background(RGB_values)
            return
        x_min = numpy.rand.randint(0,width-box_size)
        y_min = numpy.random.randint(0, height-box_size)
        x_max = int(x_min + box_size)
        y_max = int(y_min + box_size)
        cropped_image = image.crop((x_min, y_min, x_max, y_max))
        cropped_image.save(self.background_save_path + 'rand_background.png')
        self.add_image_background(self.background_save_path + 'rand_background.png')

    #def change_color(self, obj): make specifically for legos now

    def add_image_background(self, background_path):
        #Adds the background image regardless if cropped or color
        img = bpy.data.images.load(background_path)
        for area in bpy.context.screen.areas:
            if area.type == 'VIEW_3D':
                #space_data = area.spaces.active
                #bg = space_data.BackgroundImages.new()
                cam = bpy.context.scene.camera
                cam.data.show_background_images = True
                bg = cam.data.background_images.new()
                bg.image = img
                #cam.show_background_images = True
                break
        texture = bpy.data.textures.new("Texture.001", 'IMAGE')
        texture.image = img
        bpy.types.FreestyleLineStyle.active_texture = texture
        #bpy.context.scene.world.texture_slots[0].use_map_horizon = True

    def update_scene(self):
        #Updates scene
        #bpy.context.scene.update()
        bpy.context.view_layer.update()

    def get_camera(self):
        #Gets Camera
        return bpy.data.objects['Camera']

    def point_camera(self, camera, model_name, point=(0., 0., 0.)):
        #Points camera to object
        #point = Vector(point)
        #camera_location = camera.location
        #direction = point - camera_location
        #quaternion_rotation = direction.to_track_quat('-Z', 'Y')
        #euler_rotation = quaternion_rotation.to_euler()
        #camera.rotation_euler = euler_rotation
        target_object = bpy.data.objects[model_name]
        track_to = bpy.context.object.constraints.new('TRACK_TO')
        track_to.target = target_object
        track_to.track_axis = 'TRACK_NEGATIVE_Z'
        track_to.up_axis = 'UP_Y'

    def move_camera_randomly(self, camera, min_radius=1, max_radius=4, min_theta=15,
                             max_theta = 90):
        #Moves the camera
        radius = numpy.random.uniform(min_radius, max_radius)
        theta = numpy.random.uniform(numpy.deg2rad(min_theta), numpy.deg2rad(max_theta))
        phi = numpy.random.uniform(0, 2.*numpy.pi)
        x = radius * numpy.cos(phi) *numpy.sin(theta)
        y = radius * numpy.sin(phi) *numpy.sin(theta)
        z = radius * numpy.cos(theta)
        camera.location = (x, y, z)

    def delete_all_lamps(self):
        #Deletes all lamps
        for lamp_structure in bpy.data.lamps:
            lamp_name = lamp_structure.name
            lamp = bpy.data.objects[lamp_name]
            self.delete_object(lamp)

    def delete_object(self, obj):
        #Deletes object
        bpy.data.objects.remove(obj, do_unlink=True)

    def change_camera_perspective(self, camera, min_radius=1, max_radius=3,
                                  min_theta=15, max_theta=90, point=(0., 0., 0.,)):
        #Coordinates the movement of camera then points it
        self.move_camera_randonly(camera, min_radius, max_radius, min_theta,
                                  max_theta)
        self.point_camear(camera, point)

    def add_plane(self, radius=10, location=(0, 0, 0)):
        #Adds plane
        bpy.ops.mesh.primitive_plane_add(radius=radius, location=location)

    def change_focal_length(self, focal_length=45, camera_name='Camera'):
        #Changes the focal length of the camera
        bpy.data.cameras[camera_name].lens = focal_length

