#! /usr/bin/env morseexec

""" Basic MORSE simulation scene for the subseaIMR environment

Feel free to edit this template as you like!
"""

from morse.builder import *
import bpy
#from morse.builder.sensors import *


from subseaIMR.builder.robots import Seabotix
from subseaIMR.builder.actuators import Line
from subseaIMR.builder.sensors import Sonar
from subseaIMR.builder.sensors import Echosounder
from subseaIMR.builder.sensors import DepthSensor
from subseaIMR.builder.sensors import CollisionBoxes
from subseaIMR.builder.sensors import LBL

import numpy as np





#bpymorse.set_speed(25, 5, 5)

# Adding Videoray robot with default actuators and sensors
robot = Seabotix(Actuators=True,Sensors=True)
robot.frequency(100)

robot.thrusters.add_stream('moos','subseaIMR.middleware.moos.ThrustForces.ThrustForcesReader',moos_name='Thrusters',moos_freq=50.0)
robot.thrusters.frequency(100)
robot.fluidForces.frequency(100)

# Initial Position of robot (ENU)
robot.translate(0, 0, 1.5) 
robot.rotate(0, 0.0, 0)

line = Line()
line.frequency(25)
robot.append(line)

# Pose sensor
pose = Pose()
pose.frequency(10)
pose.alter('NED', 'subseaIMR.modifiers.ned.SFUposeToFSD')
pose.add_stream('moos','subseaIMR.middleware.moos.pose.PoseNotifier',moos_name='Pose',moos_msg_prefix='currentNEDPos_')
robot.append(pose)

# Velocity sensor
velocity=Velocity()
velocity.frequency(10)
velocity.alter('NED', 'subseaIMR.modifiers.ned.SFUvelocityToFSD')
velocity.add_stream('moos','subseaIMR.middleware.moos.velocity.VelocityNotifier',moos_name='Velocity')
robot.append(velocity)


robot.camera.properties(cam_width=960, cam_height=540, cam_focal=10, cam_far=200)
robot.camera.add_stream('socket')
#robot.camera.add_stream('moos','subseaIMR.middleware.moos.camera.CameraNotifyer',moos_name='Camera')
robot.camera.frequency(20)

# Sonar
#sonar = Sonar()
#sonar.properties(Visible_arc = False)
#sonar.translate(0,0,0.18)
#sonar.rotate(0,0,np.pi/2)
#sonar.frequency(10)

#sonar.add_stream('moos','subseaIMR.middleware.moos.sonar.SonarNotifier',moos_name='Sonar')
#robot.append(sonar)

# IMU sensor
imu = IMU()
imu.frequency(50)
imu.add_stream('moos','subseaIMR.middleware.moos.IMU.IMUNotifier',moos_name='IMUNotifier')
robot.append(imu)

# Echosounder
#echo = Echosounder()
#echo.frequency(2)
#echo.add_stream('moos','subseaIMR.middleware.moos.Echosounder.EchosounderNotifier',moos_name='Echosounder')
#robot.append(echo)

# Depth sensor
depth = DepthSensor()
depth.frequency(10)
depth.properties(offset = 15)
depth.add_stream('moos', 'subseaIMR.middleware.moos.depth.DepthNotifier',moos_name = 'DepthSensor')
robot.append(depth)

#collision = CollisionBoxes()
#collision.add_stream('moos','subseaIMR.middleware.moos.CollisionBoxes.CollisionReader',moos_name='CollisionBoxes')
#robot.append(collision)

#LBLSensor = LBL()
#LBLSensor.frequency(2)
#Positions = [(2,0,0),(0,2,0),(-2,0,0),(0,-2,1)] # ENU
#LBLSensor.add_parameters(TRANSCEIVERS=Positions)
#LBLSensor.add_stream('moos','subseaIMR.middleware.moos.LBL.LBLNotifyer',moos_name='LBLNotifyer')
#robot.append(LBLSensor)



#gyroscope.alter('NED', 'subseaIMR.modifiers.ned.AnglesToNED')

# Adding sensors and acutators to moos network
#pose.add_stream('ros', topic='Dynamics/MORSE/Pose')
#ThrustForces.add_stream('moos', 'subseaIMR.middleware.moos.ThrustForces.ThrustForcesReader', moos_name='ThrustRPMReader',moos_freq=100.0)


# Environmenst setup

# set 'fastmode' to True to switch to wireframe mode
env = Environment('subseaIMR/environments/Environment_april.blend', fastmode = False)
#env = Environment('subseaIMR/environments/Subsea_Obstacles.blend', fastmode = False)
env.set_time_strategy(TimeStrategies.BestEffort)
env.properties(rho = 1025.0, Current_velocity = 0.0, Current_heading = np.pi/2)
env.simulator_frequency(100)

# set coordinates for correct imu magnetometer values
env.properties(latitude = 63.4454871,longitude = 10.3610157, altitude = 0.0)

# set scene camera location
env.set_camera_location([0.0, 3.0, 15.0])
env.set_camera_rotation([0.0, 0.0, 0.0])
env.set_gravity(9.81)
env.set_mist_settings(depth = 25, enable = True, start = 5, falloff = 'QUADRATIC')
env.set_horizon_color(color=(0.04, 0.036, 0.061))
#bpymorse.get_context_scene().world.ambient_color = (0.04, 0.036, 0.061)
env.set_camera_clip(clip_end=150)
#bpy.data.scene["S.1280.720"].camera = robot.camera.bge_object.CameraRobot




