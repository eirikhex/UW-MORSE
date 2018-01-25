import logging; logger  =  logging.getLogger("morse." + __name__)
from subseaSintef.middleware.moos.abstract_moos import AbstractMOOS

class IMUNotifier(AbstractMOOS):
    """ notify IMU """

    def default(self,  ci = 'unused'):
        cur_time = self.time()

        vel = self.data['angular_velocity']
        acc = self.data['linear_acceleration']
        mag = self.data['magnetic_field']
        
        
        # post angular rates
        self.notify('imu_gyro_p', vel[0], cur_time)
        self.notify('imu_gyro_q', vel[1], cur_time)
        self.notify('imu_gyro_r', vel[2], cur_time)
    
        # post accelerations
        self.notify('imu_acc_x', acc[0], cur_time)
        self.notify('imu_acc_y', acc[1], cur_time)
        self.notify('imu_acc_z', acc[2], cur_time)
        
        # post magnetometer values
        self.notify('imu_mag_x', mag[0], cur_time) # North component
        self.notify('imu_mag_y', mag[1], cur_time) # East component
        self.notify('imu_mag_z', mag[2], cur_time) # Downward component
