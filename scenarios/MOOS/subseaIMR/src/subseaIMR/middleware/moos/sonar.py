import logging; logger = logging.getLogger("morse." + __name__)
from subseaIMR.middleware.moos.abstract_moos import AbstractMOOS
from morse.core import blenderapi

class SonarNotifier(AbstractMOOS):
    """ Post Sonar data to MOOSDB """

    def default(self,  ci='unused'):
        cur_time=self.time()
        
        bearing = self.data['bearing']
        bins = self.data['scan_list']
        
        # compose message
        msg = 'bearing=' + str(bearing) ;
        
        for i in range(200):
            if bins[i] == 0:
                continue
            else:
                msg += ', bin' +str(i) + '=' + str(int(bins[i]))
                
        
        # Post message to database:
        self.notify('SonarBins', msg, cur_time)
        
        msg = '[' + str(self.data['bearing']) + ';'
        for i in range(len(self.data['range_list'])):
            msg += str(self.data['range_list'][i]) + ';'
            
        msg += ']'
        
        self.notify('ranges', msg, cur_time)
        