import logging; logger = logging.getLogger("morse." + __name__)
from mathutils import Vector
import morse.core.sensor
import bpy

from morse.core.services import service, async_service
from morse.core import status
from morse.helpers.components import add_data, add_property

class CollisionBoxes(morse.core.sensor.Sensor):
    """Write here the general documentation of your sensor.
    It will appear in the generated online documentation.
    """
    _name = "CollisionBoxes"
    _short_desc = "A Pressure based underwater depth sensor. "

    add_data('collision_list', [33,66],'list', 'list of boxes with detected collisions')

    def __init__(self, obj, parent=None):
        logger.info("%s initialization" % obj.name)
        # Call the constructor of the parent class
        morse.core.sensor.Sensor.__init__(self, obj, parent)
        
        self.r = 0
        

        logger.info('Component initialized')

    def default_action(self):
        """ Main loop of the sensor.

        Implements the component behaviour
        """
        
        collisions = self.local_data['collision_list']
        print(collisions)
        green = (.0, .9, .6)
        red   = (.9, .0, .0)
        
        for i in range(0,80,10):
            for j in range(0,8):
                num  = i+j
                name = "Mat_CollisionCube_" + str(num)
                if num in collisions:
                    bpy.data.materials[name].diffuse_color = red
                else:
                    bpy.data.materials[name].diffuse_color = green
                
                
        
                
        
        #print(bpy.data.materials[:])
        #print(self._cube.materials[0])


        # implement here the behaviour of your sensor


