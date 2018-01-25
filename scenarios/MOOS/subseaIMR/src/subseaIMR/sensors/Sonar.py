import logging; logger = logging.getLogger("morse." + __name__)

from morse.core.sensor import Sensor

from morse.core.services import service, async_service
from morse.core import status
from morse.helpers.components import add_data, add_property
from morse.core import blenderapi
from morse.core import mathutils
from morse.builder import bpymorse
import morse.helpers.transformation
import numpy as np

class Sonar(Sensor):
    """Write here the general documentation of your sensor.
    It will appear in the generated online documentation.
    """
    _name = "Sonar"
    _short_desc = "A 360 degree scanning underwater scanning sonar"

    add_data('point_list', [], "list", "Array that stores the positions of \
            the points found by the laser. The points are given with respect \
            to the location of the sensor, and stored as lists of three \
            elements. The number of points depends on the geometry of the arc \
            parented to the sensor (see below). The point (0, 0, 0) means that\
            this ray has not it anything in its range", level =["raw", "rssi"] )
    add_data('range_list', [], "list", "Array that stores the distance to the \
            first obstacle detected by each ray. The order indexing of this \
            array is the same as for point_list, so that the element in the \
            same index of both lists will correspond to the measures for the \
            same ray. If the ray does not hit anything in its range it returns \
            laser_range", level =["raw", "rssi"])
    
    add_data('scan_list', [], "list", "Array that stores the distance to the \
            first obstacle detected by each ray. The order indexing of this \
            array is the same as for point_list, so that the element in the \
            same index of both lists will correspond to the measures for the \
            same ray. If the ray does not hit anything in its range it returns \
            laser_range", level =["raw", "rssi"])
    
    add_data('bearing',0,"double","Bearing of current scan_list")
    
    add_property('laser_range', 30.0, 'laser_range', "float",
                 "The distance in meters from the center of the sensor to which\
                  it is capable of detecting other objects.")
    add_property('resolution', 1.0, 'resolution', "float",
                 "The angle between each laser in the sensor. Expressed in \
                  degrees in decimal format. (i. e.), half a degree is     \
                  expressed as 0.5. Used when creating the arc object.")
    add_property('scan_window', 180.0, 'scan_window', "float",
                 "The full angle covered by the sensor. Expressed in degrees \
                  in decimal format. Used when creating the arc object.")
    add_property('visible_arc', False, 'Visible_arc', "boolean",
                 "if the laser arc should be displayed during the simulation")
    add_property('layers', 1, 'layers', "integer",
                  "Number of scanning planes used by the sensor.")
    add_property('layer_separation', 0.8, 'layer_separation', "float",
                 "The angular distance between the planes, in degrees.")
    add_property('layer_offset', 0.125, 'layer_offset', "float",
                 "The horizontal distance between the scan points in \
                  consecutive scanning layers. Must be given in degrees.")

    def __init__(self, obj, parent=None):
        """
        Constructor method.

        Receives the reference to the Blender object.
        The second parameter should be the name of the object's parent.
        """
        logger.info('%s initialization' % obj.name)
        # Call the constructor of the parent class
        Sensor.__init__(self, obj, parent)

        arc_prefix = 'Arc_'

        # Look for a child arc to use for the scans
        for child in obj.children:
            if arc_prefix in child.name:
                self._ray_arc = child
                logger.info("Sonar: Using arc object: '%s'" % self._ray_arc)
                break

        # Set its visibility, according to the settings
        self._ray_arc.setVisible(self.visible_arc)
        self._ray_list = []

        # Create an empty list to store the intersection points
        self.local_data['point_list'] = []
        self.local_data['range_list'] = []
        
        self.nBins = 300
        self.nSteps = 200
        self.stepSize = (2*np.pi)/self.nSteps
        
        # init scan list, Nbins = 300, Number og bearing steps is 200
        self.local_data['scan_list']  =  [0 for i in range(self.nBins)]
        self.bearing_index = 0


        # Get the datablock of the arc, to extract its vertices
        ray_object = blenderapi.objectdata(self._ray_arc.name)
        for vertex in ray_object.data.vertices:
            logger.debug ("Vertex %d = %s" % (vertex.index, vertex.co))

            # Skip the first vertex.
            # It is the one located at the center of the sensor
            if vertex.index == 0:
                continue

            # Store the position of the vertex in a list
            # The position is already given as a mathutils.Vector
            self._ray_list.append(vertex.co)

            # Insert empty points into the data list
            self.local_data['point_list'].append([0.0, 0.0, 0.0])
            # Insert zeros into the range list
            self.local_data['range_list'].append(0.0)

            logger.debug("RAY %d = [%.4f, %.4f, %.4f]" %
                         (vertex.index, self._ray_list[vertex.index-1][0],
                                        self._ray_list[vertex.index-1][1],
                                        self._ray_list[vertex.index-1][2]))
            
        self.rayNormalizationGain = 255.0 /len(self._ray_list) # maximum possible bin value is 255

        # Get some information to be able to deform the arcs
        if self.visible_arc:
            self._layers = 1
            if 'layers' in self.bge_object:
                self._layers = self.bge_object['layers']
            self._vertex_per_layer = len(self._ray_list) // self._layers
            
        self.arc_pos = morse.helpers.transformation.Transformation3d(None)
        
        logger.info('Component initialized, runs at %.2f Hz', self.frequency)


    def default_action(self):
        """
        Do ray tracing from the SICK object using a semicircle

        Generates a list of lists, with the points located.
        Also deforms the geometry of the arc associated to the SICK,
        as a way to display the results obtained.
        """
        #logger.debug("ARC POSITION: [%.4f, %.4f, %.4f]" %
        #                (self.bge_object.position[0],
        #                 self.bge_object.position[1],
        #                 self.bge_object.position[2]))

        # Get the inverse of the transformation matrix
        inverse = self.position_3d.matrix.inverted()

        index = 0
        last_yaw = self.arc_pos.yaw
        # 200 steps in the circle (one step is 1.8 degree)
        self.bearing_index += 1
        if self.bearing_index == self.nSteps:
            self.bearing_index = 0
            
        self.local_data['bearing'] = self.bearing_index #* self.stepSize
        
        self.arc_pos.rotation = mathutils.Euler([0.0,0.0, self.bearing_index * self.stepSize])
        
        self.local_data['scan_list'] = [0 for i in range(self.nBins)]
        
        for ray in self._ray_list:
            # Transform the ray to the current position and rotation
            #  of the sensor
            mat = self.arc_pos.transformation3d_with(self.position_3d)
            
            correct_ray = mat.matrix * ray
            

            # Shoot a ray towards the target
            target, point, normal = self.bge_object.rayCast(correct_ray, None,
                                                             self.laser_range,"",0,0,0)

            #logger.debug("\tTarget, point, normal: %s, %s, %s" %
            #               (target, point, normal))
            # Register when an intersection occurred
            if target:
                distance = self.bge_object.getDistanceTo(point)
                # Return the point to the reference of the sensor
                new_point = inverse * point
                
                ray_vec = self.position_3d.translation - point
                ray_vec.normalize()
                echo_intensity = ray_vec.dot(normal)
                if echo_intensity < 0:
                    print(echo_intensity)
                
                bin = int((distance/self.laser_range) * self.nBins)
                
                self.local_data['scan_list'][bin] += echo_intensity * self.rayNormalizationGain
                

                #logger.debug("\t\tGOT INTERSECTION WITH RAY: [%.4f, %.4f, %.4f]" % (correct_ray[0], correct_ray[1], correct_ray[2]))
                #logger.debug("\t\tINTERSECTION AT: [%.4f, %.4f, %.4f] = %s" % (point[0], point[1], point[2], target))
            # If there was no intersection, store the default values
            else:
                distance = self.laser_range
                new_point = [0.0, 0.0, 0.0]
                correct_ray.normalize()
                new_point = inverse * (correct_ray * self.laser_range)
                

            # Save the information gathered
            self.local_data['point_list'][index] = new_point[:]
            self.local_data['range_list'][index] = distance
            index += 1
            
        # Modify arc drawing    
        self.change_arc()


    def change_arc(self):
        # Change the shape of the arc to show what the sensor detects
        # Display only for 1 layer scanner
        if (2, 65, 0) < blenderapi.version() <= (2, 66, 3):
            # see http://projects.blender.org/tracker/?func=detail&aid=34550
            return # not supported in 2.66 due to BGE bug #34550
        # TODO rework the LDMRS (3 layers) display [code in 1.0-beta2]
        if self.visible_arc:
            for mesh in self._ray_arc.meshes:
                for m_index in range(len(mesh.materials)):
                    index = 0
                    for v_index in range(mesh.getVertexArrayLength(m_index)):
                        # Switch to a new layer after a set number of vertices
                        if index % self._vertex_per_layer == 0:
                            index += 1

                        # Skip the first vertex of a triangle. It will always
                        #  be at the origin, and should not be changed
                        if v_index % 3 == 0:
                            continue

                        # Place the next vertex in the triangle
                        if v_index % 3 == 2:
                            point = self.local_data['point_list'][index]
                            if point == [0.0, 0.0, 0.0]:
                                # If there was no intersection, move the vertex
                                # to the laser range
                                point = self._ray_list[index] * self.laser_range
                            vertex = mesh.getVertex(m_index, v_index)
                            vertex.setXYZ(point)
                            index += 1

                        # Set the final vertex, in the correct order to have
                        #  the normals facing upwards.
                        if v_index % 3 == 1:
                            point = self.local_data['point_list'][index-1]
                            if point == [0.0, 0.0, 0.0]:
                                # If there was no intersection, move the vertex
                                # to the laser range
                                point = self._ray_list[index-1] * self.laser_range
                            vertex = mesh.getVertex(m_index, v_index)
                            vertex.setXYZ(point)
                            