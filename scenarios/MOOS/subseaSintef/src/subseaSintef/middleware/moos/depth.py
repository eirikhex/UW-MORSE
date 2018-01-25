import logging; logger = logging.getLogger("morse." + __name__)
from subseaSintef.middleware.moos.abstract_moos import AbstractMOOS

class DepthNotifier(AbstractMOOS):
    """ Notify echosounder range """

    def default(self,  ci='unused'):
        cur_time=self.time()
        
        depth = self.data['depth']
        
        # post the robot position
        self.notify('currentDepth', depth, cur_time)