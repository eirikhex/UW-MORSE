import logging; logger = logging.getLogger("morse." + __name__)
from subseaIMR.middleware.moos.abstract_moos import AbstractMOOS

class EchosounderNotifier(AbstractMOOS):
    """ Notify echosounder range """

    def default(self,  ci='unused'):
        cur_time=self.time()
        
        range = self.data['range']
        
        # post the robot position
        self.notify('currentHeight', range, cur_time)