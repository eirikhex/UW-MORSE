from morse.builder.creator import SensorCreator
from morse.builder.blenderobjects import *
import logging; logger = logging.getLogger("morse." + __name__)

class Sonar(SensorCreator):
    _classpath = "subseaIMR.sensors.Sonar.Sonar"
    _blendname = "Sonar"

    def __init__(self, name=None):
        SensorCreator.__init__(self, name)
        self.properties(Visible_arc = True, laser_range = 30.0,
                scan_window = 3.0, resolution = 0.25, layers = 100,
                layer_separation = 0.35, layer_offset = 0)
        mesh = Cube("SonarCube")
        mesh.scale = (.02, .02, .02)
        mesh.color(.8, .8, .8)
        self.append(mesh)
        # set the frequency to 4 Hz
        self.frequency(20)

    
    def get_ray_material(self):
        if 'RayMat' in bpymorse.get_materials():
            return bpymorse.get_material('RayMat')

        ray_material = bpymorse.create_new_material()
        ray_material.diffuse_color = (.9, .05, .2)
        ray_material.use_shadeless = True
        ray_material.use_raytrace = False # ? is it needed ?
        ray_material.use_cast_buffer_shadows = False # ? is it needed ?
        ray_material.use_cast_approximate = False # ? is it needed ?
        ray_material.use_transparency = True
        #ray_material.transparency_method = 'Z_TRANSPARENCY'
        ray_material.alpha = 0.3
        ray_material.game_settings.use_backface_culling = False
        ray_material.name = 'RayMat'
        # link material to object as: Arc_XXX.active_material = ray_material
        return ray_material

    def create_laser_arc(self):
        """ Create an arc for use with the laserscanner sensor

        The arc is created using the parameters in the laserscanner Empty.
        'resolution and 'scan_window' are used to determine how many points
        will be added to the arc.
        """
        scene = bpymorse.get_context_scene()
        laserscanner_obj = self._bpy_object

        # Delete previously created arc
        for child in laserscanner_obj.children:
            if child.name.startswith("Arc_"):
                scene.objects.unlink( child )

        # Read the parameters to create the arc
        properties = laserscanner_obj.game.properties
        resolution = properties['resolution'].value
        window = properties['scan_window'].value
        # Parameters for multi layer sensors
        try:
            layers = properties['layers'].value
            layer_separation = properties['layer_separation'].value
            layer_offset = properties['layer_offset'].value
            laser_range = properties['laser_range'].value
        except KeyError as detail:
            layers = 1
            layer_separation = 0.0
            layer_offset = 0.0
            laser_range = 1
        logger.debug ("Creating %d arc(s) of %.2f degrees, resolution %.2f" % \
                      (layers, window, resolution))
        mesh = bpymorse.new_mesh( "ArcMesh" )
        # Add the center vertex to the list of vertices
        verts = [ [0.0, 0.0, 0.0] ]
        faces = []
        vertex_index = 0

        # Set the vertical angle, in case of multiple layers
        if layers > 1:
            v_angle = layer_separation * (layers-1) / 2.0
        else:
            v_angle = 0.0

        # Initialise the parameters for every layer
        for layer_index in range(layers):
            start_angle = -window / 2.0
            end_angle = window / 2.0
            # Offset the consecutive layers
            if (layer_index % 2) == 0:
                start_angle += layer_offset
                end_angle += layer_offset
            logger.debug ("Arc from %.2f to %.2f" % (start_angle, end_angle))
            logger.debug ("Vertical angle: %.2f" % v_angle)
            arc_angle = start_angle

            # Create all the vertices and faces in a layer
            while arc_angle <= end_angle:
                # Compute the coordinates of the new vertex
                new_vertex =  [ math.cos(math.radians(arc_angle)) * 300,
                                math.sin(math.radians(arc_angle)) * 300,
                                math.sin(math.radians(v_angle)) * 300]
                verts.append(new_vertex)
                vertex_index += 1
                # Add the faces after inserting the 2nd vertex
                if arc_angle > start_angle:
                    faces.append([0, vertex_index-1, vertex_index])
                # Increment the angle by the resolution
                arc_angle = arc_angle + resolution

            v_angle -= layer_separation
        
        # faces is vertex indexes of a face
        mesh.from_pydata( verts, [], faces )
        mesh.update()
        # Compose the name of the arc
        arc_name = "Arc_%d" % window
        arc = bpymorse.new_object( arc_name, mesh )
        arc.data = mesh
        # Remove collision detection for the object
        arc.game.physics_type = 'NO_COLLISION'
        arc.hide_render = True
        # Link the new object in the scene
        scene.objects.link( arc )
        # Set the parent to be the laserscanner Empty
        arc.parent = laserscanner_obj
        # Set the material of the arc
        arc.active_material = self.get_ray_material()
        return arc

    def after_renaming(self):
        arc = [child for child in self._bpy_object.children
               if child.name.startswith("Arc_")]
        if not arc:
            self.create_laser_arc()