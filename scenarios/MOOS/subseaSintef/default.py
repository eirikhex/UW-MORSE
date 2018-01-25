#! /usr/bin/env morseexec

""" Basic MORSE simulation scene for the subseaSintef environment

Feel free to edit this template as you like!
"""

from morse.builder import *
#from morse.builder.sensors import *


from subseaSintef.builder.robots import Seabotix
from subseaSintef.builder.actuators import Line
from subseaSintef.builder.sensors import Sonar
from subseaSintef.builder.sensors import Echosounder
from subseaSintef.builder.sensors import DepthSensor

import numpy as np





#bpymorse.set_speed(100, 5, 5)

# Adding Videoray robot with default actuators and sensors
robot = Seabotix(Actuators=True,Sensors=True)

robot.thrusters.add_stream('moos','subseaSintef.middleware.moos.ThrustForces.ThrustForcesReader',moos_name='Thrusters',moos_freq=60.0)

# Initial Position of robot (ENU)
robot.translate(0, 0, 1.5)  #TODO water plane should be z=0 also in MORSE. 
robot.rotate(0, 0.0, 0)

line = Line()
robot.append(line)

# Pose sensor
pose = Pose()
pose.alter('NED', 'subseaSintef.modifiers.ned.SFUposeToFSD')
pose.add_stream('moos','subseaSintef.middleware.moos.pose.PoseNotifier',moos_name='Pose',moos_msg_prefix='currentNEDPos_')
robot.append(pose)

# Velocity sensor
velocity=Velocity()
velocity.alter('NED', 'subseaSintef.modifiers.ned.SFUvelocityToFSD')
velocity.add_stream('moos','subseaSintef.middleware.moos.velocity.VelocityNotifier',moos_name='Velocity')
robot.append(velocity)

# Sonar
#sonar = Sonar()
#sonar.properties(Visible_arc = False)
#sonar.translate(0,0,0.18)
#sonar.rotate(0,0,np.pi/2)

#sonar.add_stream('moos','subseaSintef.middleware.moos.sonar.SonarNotifier',moos_name='Sonar')
#robot.append(sonar)

# IMU sensor
imu = IMU()
imu.frequency(100)
imu.add_stream('moos','subseaSintef.middleware.moos.IMU.IMUNotifier',moos_name='IMUNotifier')
robot.append(imu)

# Echosounder
echo = Echosounder()
echo.add_stream('moos','subseaSintef.middleware.moos.Echosounder.EchosounderNotifier',moos_name='Echosounder')
robot.append(echo)

# Depth sensor
depth = DepthSensor()
depth.properties(offset = 1.5)
depth.add_stream('moos', 'subseaSintef.middleware.moos.depth.DepthNotifier',moos_name = 'DepthSensor')
robot.append(depth)



#gyroscope.alter('NED', 'subseaIMR.modifiers.ned.AnglesToNED')

# Adding sensors and acutators to moos network
#pose.add_stream('ros', topic='Dynamics/MORSE/Pose')
#ThrustForces.add_stream('moos', 'subseaIMR.middleware.moos.ThrustForces.ThrustForcesReader', moos_name='ThrustRPMReader',moos_freq=100.0)


# Environmenst setup

# set 'fastmode' to True to switch to wireframe mode
env = Environment('subseaSintef/environments/subseaIMR.blend', fastmode = False)
env.set_time_strategy(TimeStrategies.BestEffort)
env.properties(rho = 1025.0, Current_velocity = 0.0, Current_heading = np.pi/2)
env.simulator_frequency(100)

# set coordinates for correct imu magnetometer values
env.properties(latitude = 63.4454871,longitude = 10.3610157, altitude = 0.0)

# set scene camera location
env.set_camera_location([0.0, 3.0, 15.0])
env.set_camera_rotation([0.0, 0.0, 0.0])
env.set_gravity(9.81)
env.set_mist_settings(depth = 50, enable = True, start = 5, falloff = 'QUADRATIC')
env.set_horizon_color(color=(0.05, 0.22, 0.4))
env.set_camera_clip(clip_end=150) 



