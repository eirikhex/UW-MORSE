import logging; logger = logging.getLogger("morse." + __name__)
from subseaIMR.middleware.moos.abstract_moos import AbstractMOOS

class LBLNotifyer(AbstractMOOS):
    
    def default(self, ci = 'unused'):
        cur_time = self.time()
        index = 0
        for point in self.data['RangeList']:
            self.notify(str(index)+'Range', self.data['RangeList'][index], cur_time)
            index += 1
