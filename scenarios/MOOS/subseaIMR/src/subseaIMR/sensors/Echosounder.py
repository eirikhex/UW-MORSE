import logging; logger = logging.getLogger("morse." + __name__)

import morse.core.sensor

from morse.core.services import service, async_service
from morse.core import status
from morse.helpers.components import add_data, add_property

class Echosounder(morse.core.sensor.Sensor):
    """Write here the general documentation of your sensor.
    It will appear in the generated online documentation.
    """
    _name = "Echosounder"
    _short_desc = "Acoustic range sensor to compute distance to seafloor"

    add_data('range', 0.0, "float", 'Range measured')
    add_property('_max_range', 30.0, "MaxRange", "float", 
                 "Maximum range distance."
                 "If nothing is detected, return zero")

    def __init__(self, obj, parent=None):
        logger.info("%s initialization" % obj.name)
        # Call the constructor of the parent class
        morse.core.sensor.Sensor.__init__(self, obj, parent)

        # Do here sensor specific initializations

        self._distance = 0 # dummy internal variable, for testing purposes

        logger.info('Component initialized')


    def default_action(self):
        """ 
        Send a laser directly underneath and check the position of what it hits.
        """
        target = self.position_3d.translation
        target[2] -= 1.0

        _, point, _ = self.bge_object.rayCast(target, None, self._max_range)
        logger.debug("Echosounder points to %s and hits %s" % (target, point))
        if point:
            self.local_data['range'] = self.bge_object.getDistanceTo(point)
        else:
            self.local_data['range'] = 0

