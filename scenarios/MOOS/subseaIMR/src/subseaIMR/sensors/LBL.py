import logging; logger = logging.getLogger("morse." + __name__)

import morse.core.sensor

from morse.core.services import service, async_service
from morse.core import status
from morse.helpers.components import add_data, add_property

class LBL(morse.core.sensor.Sensor):
    """An acustic sensor that measure the distance from at least four transceivers placed on the seabed to the sensor mounted on the robot.
    """
    _name = "LBL"
    _short_desc = "LBL sensor"

    # define here the data fields exported by your sensor
    # format is: field name, default initial value, type, description
    add_data('RangeList', [], "list", "A list of distances from transceivers to sensor on robot")
    def __init__(self, obj, parent=None):
        logger.info("%s initialization" % obj.name)
        # Call the constructor of the parent class
        morse.core.sensor.Sensor.__init__(self, obj, parent)

        # Do here sensor specific initializations
        try:
            from parameters import p
            SensorData = p[self.bge_object.name]
        except:
            SensorData = {}

        if 'TRANSCEIVERS' in SensorData:
            self.Transceivers = SensorData['TRANSCEIVERS']
        else:
            self.Transceivers = {}
        # Do here sensor specific initializations
        self.local_data['RangeList'] = []
        for point in self.Transceivers:
            self.local_data['RangeList'].append(0.0)
        logger.info('Component initialized')

    @service
    def default_action(self):
        """ Main loop of the sensor.

        Implements the component behaviour
        """
        index = 0
        for point in self.Transceivers:
            distance = self.bge_object.getDistanceTo(point)
            self.local_data['RangeList'][index] = distance
            index += 1

