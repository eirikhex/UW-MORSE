import logging; logger = logging.getLogger("morse." + __name__)
from subseaSintef.middleware.moos.abstract_moos import AbstractMOOS
from morse.core import blenderapi

class PoseNotifier(AbstractMOOS):
    """ Notify Pose """
    
    def initialize(self):
        AbstractMOOS.initialize(self)
        
        self.prefix = self.kwargs.get('moos_msg_prefix', 'currentPos_')

    def default(self,  ci='unused'):
        cur_time=self.time()

        # post the robot position
        self.notify(self.prefix + 'x', self.data['x'], cur_time)
        self.notify(self.prefix + 'y', self.data['y'], cur_time)
        self.notify(self.prefix + 'z', self.data['z'], cur_time)
        self.notify(self.prefix + 'rx', self.data['roll'], cur_time)
        self.notify(self.prefix + 'ry', self.data['pitch'], cur_time)
        self.notify(self.prefix + 'rz', self.data['yaw'], cur_time)
        
        ## Helm variables
        self.notify('NAV_X', self.data['y'], cur_time)
        self.notify('NAV_Y', self.data['x'], cur_time)
        self.notify('NAV_HEADING',(180 * self.data['yaw'])/3.14159265359, cur_time)
        