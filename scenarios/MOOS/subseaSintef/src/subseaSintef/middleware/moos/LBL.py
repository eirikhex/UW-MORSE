import logging; logger = logging.getLogger("morse." + __name__)
import pymoos.MOOSCommClient
from morse.middleware.moos import AbstractMOOS

class LBLNotifyer(AbstractMOOS):
    def default(self, ci = 'unused'):
        cur_time = pymoos.MOOSCommClient.MOOSTime()
        index = 0
        for point in self.data['RangeList']:
            self.m.Notify(str(index)+'Range', self.data['RangeList'][index], cur_time)
            index += 1
