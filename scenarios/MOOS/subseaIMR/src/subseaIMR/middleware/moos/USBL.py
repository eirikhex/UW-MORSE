import logging; logger = logging.getLogger("morse." + __name__)
import pymoos.MOOSCommClient
from morse.middleware.moos import AbstractMOOS

class USBLNotifyer(AbstractMOOS):

    def default(self, ci = 'unused'):
        cur_time = pymoos.MOOSCommClient.MOOSTime()
        self.m.Notify('Range', self.data['Range'][0], cur_time)
