import logging; logger  =  logging.getLogger("morse." + __name__)
import pymoos.MOOSCommClient
from morse.middleware.moos import AbstractMOOS

class IMUNotifier(AbstractMOOS):
    """ Notify IMU """

    def default(self,  ci = 'unused'):
        cur_time = pymoos.MOOSCommClient.MOOSTime()

        vel = self.data['angular_velocity']
        acc = self.data['linear_acceleration']
        # post angular rates
        self.m.Notify('zGyroP', vel[0], cur_time)
        self.m.Notify('zGyroQ', vel[1], cur_time)
        self.m.Notify('zGyroR', vel[2], cur_time)

        # post accelerations
        self.m.Notify('zAccelX', acc[0], cur_time)
        self.m.Notify('zAccelY', acc[1], cur_time)
        self.m.Notify('zAccelZ', acc[2], cur_time)
