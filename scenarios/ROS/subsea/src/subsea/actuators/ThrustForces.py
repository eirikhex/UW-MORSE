import logging; logger = logging.getLogger("morse." + __name__)
import morse.core.blenderapi
import morse.core.actuator

import bpy
import time

from morse.core.services import service, async_service, interruptible
from morse.core import status, blenderapi
from morse.helpers.components import add_data, add_property

import numpy
import scipy
import math



class Thrustforces(morse.core.actuator.Actuator):
    """Write here the general documentation of your actuator.
    It will appear in the generated online documentation.
    """
    _name = "Thrustforces"
    _short_desc = "Adds thrust forces to an underwater robot"

    # define here the data fields required by your actuator
    # format is: field name, initial value, type, description
    add_data('RPM', numpy.matrix([0, 0, 0, 0, 0, 0]),'numpy.matrix', 'Thrust force for each thruster')

    def __init__(self, obj, parent=None):
        logger.info("%s initialization" % obj.name)
        # Call the constructor of the parent class
        morse.core.actuator.Actuator.__init__(self, obj, parent)

        # Do here actuator specific initializations
        self.robot = self.robot_parent.bge_object

        self.pose3d=self.robot_parent.position_3d

        self.nu=numpy.matrix([0.0,0.0,0.0,0.0,0.0,0.0]).T
        self.robot_parent.RPM=numpy.matrix([0.0,0.0,0.0,0.0,0.0])


        try:
            from parameters import p
            ThrustParameters = p[self.bge_object.name]
        except:
            ThrustParameters = {}

        if 'nThrusters' in ThrustParameters:
            self.nThrusters   = int(ThrustParameters['nThrusters'])
        else:
            self.nThrusters   = 1

        if 'thruster_diameter' in ThrustParameters:
            self.thruster_diameter = numpy.matrix(ThrustParameters['thruster_diameter'])
        else:
            self.thruster_diameter = numpy.zeros((self.nThrusters))

        if 'RPM_limits' in ThrustParameters:
            self.RPM_limits   = numpy.matrix(ThrustParameters['RPM_limits'])
        else:
            self.RPM_limits   = numpy.zeros((2,self.nThrusters))

        if 'thrust_coeff' in ThrustParameters:
            self.thrust_coeff   = numpy.matrix(ThrustParameters['thrust_coeff'])
        else:
            self.thrust_coeff   = numpy.zeros((2,4))
        if 'thrustloss_factors' in ThrustParameters:
            self.thrustloss_factors   = numpy.matrix(ThrustParameters['thrustloss_factors'])
        else:
            self.thrustloss_factors  = numpy.zeros((2,self.nThrusters))
        if 'T' in ThrustParameters:
            self.T   = numpy.matrix(ThrustParameters['T'])
        else:
            self.T = numpy.zeros((6,self.nThrusters))     

        self.thrust=numpy.zeros((self.nThrusters, 1))
        self.RPM=numpy.zeros((self.nThrusters, 1))
        
        # TODO subscriber should be generalized ( such that we can not only use control info from ROS, but also other frameworks)
        # rospy.Subscriber("RPMcontrol/DP", Float32MultiArray, self.callback, queue_size=1)
        #rospy.Subscriber("RPMcontrol/Path", Float32MultiArray, self.callback, queue_size=1)
        #self.nu_morse = open('nu_morse.txt','w')


        logger.info('Component initialized')



    def _get_thrust(self, RPM, RPM_limits, rho, nu, thruster_diameter, thrust_coeff, thrustloss_factors, nThrusters):


      #TODO: current simulation
      nu_rel=nu

      thrust=numpy.zeros((nThrusters, 1))

      #Estimate V_a
      V_a=math.sqrt(float(nu_rel[0])*float(nu_rel[0])+float(nu_rel[1])*float(nu_rel[1]))

      for i in range (0, nThrusters):

        #Finding n
        RPM_sat=min(max(RPM[0, i], RPM_limits[1, i]), RPM_limits[0, i])
        n=float(RPM_sat/60)
        
        #Calculating J
        if(n>-0.1 and n<0.1):
          J=0
        else:
          J=V_a/(n*thruster_diameter[0, i])

        #Calculate thrust coefficient K_t
        if(n>0):
          p=0
        else:
          p=1
      
        if (J>0.525 or J<-0.484):  #TODO fjern hardkoding, få med i inputfil
          K_t=0
        else:
          K_t=thrust_coeff[p, 0]*J*J*J+thrust_coeff[p, 1]*J*J+thrust_coeff[p, 2]*J+thrust_coeff[p, 3]

        #Estimated thrust for all thrusters [N]
        thrust[i, 0]=K_t*rho*math.pow(float(thruster_diameter[0, i]), 4)*abs(n)*n*thrustloss_factors[p, i]
    
      return thrust


    def _thrust_allocation(self, f, T):
      localForce=T*f  #This is with z down!
      #localForce=numpy.matrix([10.0, 0.0, 0.0, 0.0, 0.0, 0.0]).T   #FOR TESTING DIFFERENT FORCES 

      #Difference between local coordinate frame in MORSE and ROS
      MorseForce=numpy.matrix([0.0, 0.0, 0.0, 0.0, 0.0, 0.0]).T
      MorseForce[0] =localForce[1]
      MorseForce[1] =localForce[0]
      MorseForce[2] =-localForce[2]

      MorseForce[3] =localForce[4]
      MorseForce[4] =localForce[3]
      MorseForce[5] =-localForce[5]
 
    
      return MorseForce


    def default_action(self):
        """ Main loop of the actuator.

        Implements the component behaviour
        """

        #TODO read controller path from file. Fjern hardkoding


        self.nu=self.robot_parent.nu
        
        #self.nu.T.tofile(self.nu_morse, "\t")
        #self.nu_morse.write("\n")

        self.thrust=self._get_thrust(self.local_data['RPM'], self.RPM_limits, 1025, self.nu, self.thruster_diameter, self.thrust_coeff, self.thrustloss_factors, self.nThrusters)

        localForce=self._thrust_allocation(self.thrust, self.T)

        force  = localForce[0:3].T.tolist()[0]
        torque = localForce[3:6].T.tolist()[0]
        
        self.robot.applyExternalForce(force,True)
        self.robot.applyExternalTorque(torque,True)

