import logging; logger = logging.getLogger("morse." + __name__)

import morse.core.sensor

from morse.core.services import service, async_service
from morse.core import status
from morse.helpers.components import add_data, add_property

class Depthsensor(morse.core.sensor.Sensor):
    """Write here the general documentation of your sensor.
    It will appear in the generated online documentation.
    """
    _name = "Depthsensor"
    _short_desc = "A Pressure based underwater depth sensor. "

    add_data('depth', 0.0, 'float', 'Depth under sealevel in meters')
    
    add_property('offset',0.0,'offset','float','Offset between simulation origin z, and sea-level')
    

    def __init__(self, obj, parent=None):
        logger.info("%s initialization" % obj.name)
        # Call the constructor of the parent class
        morse.core.sensor.Sensor.__init__(self, obj, parent)

        logger.info('Component initialized')

    def default_action(self):
        """ Main loop of the sensor.

        Implements the component behaviour
        """

        import random

        # implement here the behaviour of your sensor

        self.local_data['depth'] = -self.position_3d.z + self.offset # distance along X in world coordinates

