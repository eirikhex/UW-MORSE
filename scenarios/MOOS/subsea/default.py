#! /usr/bin/env morseexec

""" Basic MORSE simulation scene for <subsea> environment

Feel free to edit this template as you like!
"""

from morse.builder import *
from morse.builder.sensors import Velocity
from subsea.builder.sensors import LBL
from subsea.builder.sensors import USBL
from subsea.builder.robots import Underwaterrobot
from subsea.builder.actuators import FluidForces
from subsea.builder.actuators import Thrustforces 
from subsea.builder.robots import Thirtyk
import numpy as np
from nav_msgs.msg import Odometry



bpymorse.set_speed(24, 5, 5)

robot = Thirtyk()
robot.set_rigid_body()
robot.set_collision_bounds()

########################################################
################   GET SPECIFICATIONS   ################ TODO: Do this in separate file  
########################################################

file=open("inputFile.txt", "r")
lines=file.readlines()
print("reading file ", file.name)
print("Specifications for   ", lines[2])

#initial pose
dummy=lines[4].split()
poseNED=[float(dummy[0]), float(dummy[1]), float(dummy[2]), float(dummy[3]), float(dummy[4]), float(dummy[5])]
poseENU=[poseNED[1], poseNED[0], -poseNED[2], poseNED[4], poseNED[3], -poseNED[5]] 
print("Initial pose(NED) set to:  ", poseNED)

#initial velocity
dummy=lines[6].split()
velocity=[float(dummy[0]), float(dummy[1]), float(dummy[2]), float(dummy[3]), float(dummy[4]), float(dummy[5])]
print("Initial velocity is ", velocity)
#TODO: Set ROV initial velocity to the values obtained here

#Mass Matrix
dummy1=lines[8].split()
dummy2=lines[9].split()
dummy3=lines[10].split()
dummy4=lines[11].split()
dummy5=lines[12].split()
dummy6=lines[13].split()
MassMatrix=[[float(dummy1[0]), float(dummy1[1]), float(dummy1[2]), float(dummy1[3]), float(dummy1[4]), float(dummy1[5])],   
     [float(dummy2[0]), float(dummy2[1]), float(dummy2[2]), float(dummy2[3]), float(dummy2[4]), float(dummy2[5])],
     [float(dummy3[0]), float(dummy3[1]), float(dummy3[2]), float(dummy3[3]), float(dummy3[4]), float(dummy3[5])],
     [float(dummy4[0]), float(dummy4[1]), float(dummy4[2]), float(dummy4[3]), float(dummy4[4]), float(dummy4[5])],
     [float(dummy5[0]), float(dummy5[1]), float(dummy5[2]), float(dummy5[3]), float(dummy5[4]), float(dummy5[5])], 
     [float(dummy6[0]), float(dummy6[1]), float(dummy6[2]), float(dummy6[3]), float(dummy6[4]), float(dummy6[5])]]

print("M_rb set to \n ", MassMatrix)


#Added mass matrix
dummy1=lines[15].split()
dummy2=lines[16].split()
dummy3=lines[17].split()
dummy4=lines[18].split()
dummy5=lines[19].split()
dummy6=lines[20].split()
M_a=[[float(dummy1[0]), float(dummy1[1]), float(dummy1[2]), float(dummy1[3]), float(dummy1[4]), float(dummy1[5])],   
     [float(dummy2[0]), float(dummy2[1]), float(dummy2[2]), float(dummy2[3]), float(dummy2[4]), float(dummy2[5])],
     [float(dummy3[0]), float(dummy3[1]), float(dummy3[2]), float(dummy3[3]), float(dummy3[4]), float(dummy3[5])],
     [float(dummy4[0]), float(dummy4[1]), float(dummy4[2]), float(dummy4[3]), float(dummy4[4]), float(dummy4[5])],
     [float(dummy5[0]), float(dummy5[1]), float(dummy5[2]), float(dummy5[3]), float(dummy5[4]), float(dummy5[5])], 
     [float(dummy6[0]), float(dummy6[1]), float(dummy6[2]), float(dummy6[3]), float(dummy6[4]), float(dummy6[5])]]
print(" Added mass is set to: \n", M_a)


#Linear damping matrix
dummy1=lines[22].split()
dummy2=lines[23].split()
dummy3=lines[24].split()
dummy4=lines[25].split()
dummy5=lines[26].split()
dummy6=lines[27].split()
D_lin=[[float(dummy1[0]), float(dummy1[1]), float(dummy1[2]), float(dummy1[3]), float(dummy1[4]), float(dummy1[5])],   
     [float(dummy2[0]), float(dummy2[1]), float(dummy2[2]), float(dummy2[3]), float(dummy2[4]), float(dummy2[5])],
     [float(dummy3[0]), float(dummy3[1]), float(dummy3[2]), float(dummy3[3]), float(dummy3[4]), float(dummy3[5])],
     [float(dummy4[0]), float(dummy4[1]), float(dummy4[2]), float(dummy4[3]), float(dummy4[4]), float(dummy4[5])],
     [float(dummy5[0]), float(dummy5[1]), float(dummy5[2]), float(dummy5[3]), float(dummy5[4]), float(dummy5[5])], 
     [float(dummy6[0]), float(dummy6[1]), float(dummy6[2]), float(dummy6[3]), float(dummy6[4]), float(dummy6[5])]]
print(" Linear damping matrix is set to: \n", D_lin)


#Quadratic damping matrix
dummy1=lines[29].split()
dummy2=lines[30].split()
dummy3=lines[31].split()
dummy4=lines[32].split()
dummy5=lines[33].split()
dummy6=lines[34].split()
D_quad=[[float(dummy1[0]), float(dummy1[1]), float(dummy1[2]), float(dummy1[3]), float(dummy1[4]), float(dummy1[5])],   
     [float(dummy2[0]), float(dummy2[1]), float(dummy2[2]), float(dummy2[3]), float(dummy2[4]), float(dummy2[5])],
     [float(dummy3[0]), float(dummy3[1]), float(dummy3[2]), float(dummy3[3]), float(dummy3[4]), float(dummy3[5])],
     [float(dummy4[0]), float(dummy4[1]), float(dummy4[2]), float(dummy4[3]), float(dummy4[4]), float(dummy4[5])],
     [float(dummy5[0]), float(dummy5[1]), float(dummy5[2]), float(dummy5[3]), float(dummy5[4]), float(dummy5[5])], 
     [float(dummy6[0]), float(dummy6[1]), float(dummy6[2]), float(dummy6[3]), float(dummy6[4]), float(dummy6[5])]]
print("Quadratic damping matrix is set to: \n", D_quad)


#Centre of Gravity
dummy=lines[36].split()
COG=[float(dummy[0]), float(dummy[1]), float(dummy[2])]


#Centre of Buoyancy
dummy=lines[38].split()
COB=[float(dummy[0]), float(dummy[1]), float(dummy[2])]


#ROV Volume
Volume=float(lines[40])
print("Volume is ", Volume)

#Thruster allocations
thrusterN=int(lines[42])
ThrustAll=[[0 for x in range(thrusterN)] for x in range(6)]
print("Number of thrusters:  ", thrusterN)
dummy1=lines[44].split()
dummy2=lines[45].split()
dummy3=lines[46].split()
dummy4=lines[47].split()
dummy5=lines[48].split()
dummy6=lines[49].split()

for i in range (0, thrusterN):
  ThrustAll[0][i]=float(dummy1[i])
  ThrustAll[1][i]=float(dummy2[i])
  ThrustAll[2][i]=float(dummy3[i])
  ThrustAll[3][i]=float(dummy4[i])
  ThrustAll[4][i]=float(dummy5[i])
  ThrustAll[5][i]=float(dummy6[i])

#Diameters
dummy=lines[51].split()
diameters=[]
for i in range (0, thrusterN):
  diameters.append(float(dummy[i]))
  
print("Diameter for thrusters: ")
print(diameters)


#Thrust coefficient function
dummy1=lines[53].split()
dummy2=lines[54].split()
K_t=[[float(dummy1[0]), float(dummy1[1]), float(dummy1[2]), float(dummy1[3])],[float(dummy2[0]), float(dummy2[1]), float(dummy2[2]), float(dummy2[3])]]
print("thrust coeff function:")
print("K_t= ", K_t[0][0], " J³ + ", K_t[0][1], " J² +", K_t[0][2], " J +", K_t[0][3], "\t \t (n>0)")
print("K_t= ", K_t[1][0], " J³ + ", K_t[1][1], " J² +", K_t[1][2], " J +", K_t[1][3], "\t \t (n<0)")

#Thrust loss factors
dummy1=lines[56].split()
dummy2=lines[57].split()
theta=[[0 for x in range(thrusterN)] for x in range(2)]
for i in range (0, thrusterN):
  theta[0][i]=float(dummy1[i])
  theta[1][i]=float(dummy2[i])
print("thrust loss factors:")
print(theta)

#RPM limits
dummy1=lines[59].split()
dummy2=lines[60].split()
RPMlim=[[0 for x in range(thrusterN)] for x in range(2)]
for i in range (0, thrusterN):
  RPMlim[0][i]=float(dummy1[i])
  RPMlim[1][i]=float(dummy2[i])
print("RPM limits:")
print(RPMlim)

#TODO Read LBL and USBL from a config file
#LBL parameters
Positions = [(1,1,0),(1,-1,1),(-1,-1,0),(-1,1,0)]
#USBL parameters
Position = [(10,10,20)]

#################TODO Read controller path
file.close()
####################################################################################################################


robot.set_mass(MassMatrix[0][0])
robot.translate(poseENU[0], poseENU[1], poseENU[2])  #TODO water plane should be z=0 also in MORSE. 
robot.rotate(poseENU[3], poseENU[4], poseENU[5])

#Actuators
HydroForces = FluidForces()
ThrustForces = Thrustforces()
LBLSensor = LBL()
USBLSensor1 = USBL()
USBLSensor2 = USBL()
USBLSensor3 = USBL()
USBLSensor4 = USBL()
HydroForces.properties(V=Volume)

robot.append(ThrustForces)
robot.append(HydroForces)
robot.append(LBLSensor)
robot.append(USBLSensor1)
robot.append(USBLSensor2)
robot.append(USBLSensor3)
robot.append(USBLSensor4)


#Make parameters available for the actuators
ThrustForces.add_parameters(thruster_diameter=diameters, RPM_limits=RPMlim, thrust_coeff=K_t, thrustloss_factors=theta, nThrusters=thrusterN, T=ThrustAll)
HydroForces.add_parameters(A=M_a, M_rb=MassMatrix, D_l = D_lin, D_q=D_quad, r_g=COG, r_b=COB) #TODO include controller path
LBLSensor.add_parameters(TRANSCEIVERS=Positions)
LBLSensor.translate(x=10.0,y=10.0,z=20.0)
USBLSensor1.add_parameters(TRANSCEIVER=Position)
USBLSensor2.add_parameters(TRANSCEIVER=Position)
USBLSensor3.add_parameters(TRANSCEIVER=Position)
USBLSensor4.add_parameters(TRANSCEIVER=Position)
USBLSensor1.translate(x=1.0,y=1.0,z=0.0)
USBLSensor2.translate(x=1.0,y=-1.0,z=1.0)
USBLSensor3.translate(x=-1.0,y=-1.0,z=0.0)
USBLSensor4.translate(x=-1.0,y=1.0,z=0.0)
# Pose sensor
pose = Pose()
robot.append(pose)

# Velocity sensor
velocity=Velocity()
robot.append(velocity)

gyroscope = Gyroscope()
robot.append(gyroscope)

imu = IMU()
robot.append(imu)
# Get pose and velocity in FSD (x_Forward-y_Starboard-z_Down)
pose.alter('NED', 'subsea.modifiers.ned.SFUposeToFSD')
velocity.alter('NED', 'subsea.modifiers.ned.SFUvelocityToFSD')
#gyroscope.alter('NED', 'subsea.modifiers.ned.AnglesToNED')

# Adding sensors and acutators to moos network
#pose.add_stream('ros', topic='Dynamics/MORSE/Pose')
#velocity.add_stream('ros', topic='Dynamics/MORSE/Twist')
ThrustForces.add_stream('moos', 'subsea.middleware.moos.ThrustForces.ThrustForcesReader', moos_name='ThrustRPMReader',moos_freq=1000.0)
LBLSensor.add_stream('moos','subsea.middleware.moos.LBL.LBLNotifyer',moos_name='LBLNotifyer',moos_freq=1000.0)
USBLSensor1.add_stream('moos','subsea.middleware.moos.USBL.USBLNotifyer',moos_name='USBLSensorNotifyer0',moos_freq=1000.0)
USBLSensor2.add_stream('moos','subsea.middleware.moos.USBL.USBLNotifyer',moos_name='USBLSensorNotifyer1',moos_freq=1000.0)
USBLSensor3.add_stream('moos','subsea.middleware.moos.USBL.USBLNotifyer',moos_name='USBLSensorNotifyer2',moos_freq=1000.0)
USBLSensor4.add_stream('moos','subsea.middleware.moos.USBL.USBLNotifyer',moos_name='USBLSensorNotifyer3',moos_freq=1000.0)
gyroscope.add_stream('moos',moos_name='Gyroscope',moos_freq=1000.0)
imu.add_stream('moos','subsea.middleware.moos.IMU.IMUNotifier',moos_name='IMUNotifyer',moos_freq=1000.0)
# set 'fastmode' to True to switch to wireframe mode
env = Environment('subsea/environments/subsea.blend', fastmode = False)
#env.set_time_strategy(TimeStrategies.FixedSimulationStep)   #TODO fixed or variable? 
env.set_time_strategy(TimeStrategies.BestEffort)

env.properties(latitude = 63.4454871,longitude = 10.3610157, altitude = 0.0)

env.properties(rho = 1025.0, U = 0.0)
env.set_camera_location([10.0, -10.0, 10.0])
env.set_camera_rotation([1.05, 0, 0.78])
env.set_gravity(9.81)
env.set_mist_settings(depth = 25, enable = True, start = 5, falloff = 'QUADRATIC')
env.set_horizon_color(color=(0.05, 0.22, 0.4))
