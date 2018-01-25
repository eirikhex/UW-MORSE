import logging; logger = logging.getLogger("morse." + __name__)
from subseaSintef.middleware.moos.abstract_moos import AbstractMOOS

class VelocityNotifier(AbstractMOOS):
    """ Notify Pose """

    def default(self,  ci='unused'):
        cur_time=self.time()
        
        lin_vel = self.data['linear_velocity']
        ang_vel = self.data['angular_velocity']
        
        # post the robot position
        self.notify('currentVEHVel_u', lin_vel[0], cur_time)
        self.notify('NAV_SPEED', lin_vel[0], cur_time)
        self.notify('currentVEHVel_v', lin_vel[1], cur_time)
        self.notify('currentVEHVel_w', lin_vel[2], cur_time)
        self.notify('currentVEHVel_p', ang_vel[0], cur_time)
        self.notify('currentVEHVel_q', ang_vel[1], cur_time)
        self.notify('currentVEHVel_r', ang_vel[2], cur_time)