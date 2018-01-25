import logging; logger = logging.getLogger("morse." + __name__)

import morse.core.sensor

from morse.core.services import service, async_service
from morse.core import status
from morse.helpers.components import add_data, add_property

class USBL(morse.core.sensor.Sensor):
    """An acustic sensor that measure the distance from a transceiver placed on the seabed to the sensor mounted on the robot.
    """
    _name = "USBL"
    _short_desc = "USBL sensor"

   # define here the data fields exported by your sensor
    # format is: field name, default initial value, type, description
    add_data('Range', [], "list", "Distance from USBL transceiver to the sensor")
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

        if 'TRANSCEIVER' in SensorData:
            self.Transceiver = SensorData['TRANSCEIVER']
        else:
            self.Transceiver = {}
        # Do here sensor specific initializations
        self.local_data['Range'] = []
        self.local_data['Range'].append(0.0)
        logger.info('Component initialized')

    @service
    def default_action(self):
        """ Main loop of the sensor.

        Implements the component behaviour
        """
        distance = self.bge_object.getDistanceTo(self.Transceiver[0])
        self.local_data['Range'][0] = distance
