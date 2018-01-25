import logging; logger = logging.getLogger("morse." + __name__)
from subseaIMR.middleware.moos.abstract_moos import AbstractMOOS

class DepthNotifier(AbstractMOOS):
    """ Notify echosounder range """

    def default(self,  ci='unused'):
        cur_time=self.time()
        
        depth = self.data['depth']
        
        # post the robot position
        self.notify('currentDepth', depth, cur_time)
        self.notify('CURRENTDEPTH', depth, cur_time)