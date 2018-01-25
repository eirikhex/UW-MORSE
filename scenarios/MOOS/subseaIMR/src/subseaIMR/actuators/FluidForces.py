import logging; logger = logging.getLogger("morse." + __name__)
from morse.core import mathutils, blenderapi
import morse.core.actuator
import bpy
import bge

import numpy

import math

from morse.core.services import service, async_service, interruptible
from morse.core import status, blenderapi
from morse.helpers.components import add_data, add_property

class FluidForces(morse.core.actuator.Actuator):
    """Write here the general documentation of your actuator.
    It will appear in the generated online documentation.
    """
    _name = "Fluidforces"
    _short_desc = "Adds fluid forces to an underwater robot"

    # define here the data fields required by your actuator
    # format is: field name, initial value, type, description
    
    #property format : local name, default, BlenderProperty name, type, doc
    add_property('_V', 0.0, 'V','float','Volume')
    

    def __init__(self, obj, parent=None):
        logger.info("%s initialization" % obj.name)
        # Call the constructor of the parent class
        morse.core.actuator.Actuator.__init__(self, obj, parent)
        
        ###################################################
        #                 Initializations                 #
        ###################################################
        self.env = blenderapi.getssr()
        self.rho = self.env.get('rho')
        if not self.rho:
            self.rho = 1025
            
        
        #print(self.rho)
        # get environment gravity constant
        self.g = blenderapi.game_settings().physics_gravity
        
        # make a local reference to the bge_object of the parent robot
        self.robot = self.robot_parent.bge_object
        
        # make a local reference to the robot local linear and angular velocity
        self.v = self.robot_parent.bge_object.localLinearVelocity
        self.w = self.robot_parent.bge_object.localAngularVelocity

        #Make a local reference to the robot pose
        self.pose3d=self.robot_parent.position_3d
       

        # 6DOF rotation from enu to ned (R_etn == R_nte)
        self.R_etn = numpy.matrix([
        [0,1,0,0,0,0],
        [1,0,0,0,0,0],
        [0,0,-1,0,0,0],
        [0,0,0,0,1,0],
        [0,0,0,1,0,0],
        [0,0,0,0,0,-1]])
        
        # make a local variable for 6-DOF velocity
        self.nu = numpy.matrix([0.0,0.0,0.0,0.0,0.0,0.0]).T
        
        try:
            from parameters import p
            FluidParameters = p[self.bge_object.name]
        except:
            FluidParameters = {}
        
        if 'A' in FluidParameters:
            self.A   = numpy.matrix(FluidParameters['A'])
        else:
            self.A   = numpy.zeros((6,6))
            
        if 'M_rb' in FluidParameters:
            self.M_rb   = numpy.matrix(FluidParameters['M_rb'])
        else:
            self.M_rb   = numpy.zeros((6,6))

        if 'D_l' in FluidParameters:
            self.D_l   = numpy.matrix(FluidParameters['D_l'])
        else:
            self.D_l   = numpy.zeros((6,6))
            
        if 'D_q' in FluidParameters:
            self.D_q   = numpy.matrix(FluidParameters['D_q'])
        else:
            self.D_q   = numpy.zeros((6,6))
            
        if 'r_g' in FluidParameters:
            self.r_g   = numpy.matrix(FluidParameters['r_g']).T
        else:
            self.r_g   = numpy.zeros((3,1))
        
        if 'r_b' in FluidParameters:
            self.r_b   = numpy.matrix(FluidParameters['r_b']).T
        else:
            self.r_b   = numpy.zeros((3,1))  
            
        self.mass=self.M_rb[0, 0]
        self.I_g=self.M_rb[3:6, 3:6]

        # TODO: Get inertia from builder script
        self.totalInertia_NED = self.A + self.M_rb
        
        # Calculate total inertia in enu and set in the physics model
        self.totalInertia_ENU = self.R_etn.T * self.totalInertia_NED *self.R_etn
        self.robot.set6DOFinertia(self.totalInertia_ENU[0:3,0:3].tolist(),self.totalInertia_ENU[0:3,3:6].tolist(),self.totalInertia_ENU[3:6,0:3].tolist(),self.totalInertia_ENU[3:6,3:6].tolist())
        self.robot.enable6DOF()
        
        # Set Damping in blender to zero (linear,angular)
        self.robot.setDamping(0.0,0.0)

        # Open files TODO find better way to store information
        #self.lin_damping=open('lin_damping_morse.txt','w') 
        #self.quad_damping=open('quad_damping_morse.txt', 'w')
        #self.coriolis_a=open('coriolis_a_morse.txt', 'w')
        #self.coriolis_rb=open('coriolis_rb_morse.txt', 'w')
        #self.nu_morse=open('nu_morse.txt', 'w')

        #Set init time
        #self.time=time=morse.core.blenderapi.persistantstorage().time.time
        #self.time_init=self.time     
        #self.begin=1

        #Set buoyancy force
        self.robot.setBuoyancy([0, 0, self._V*self.rho*self.g])

    def setV(self,V):
        self.V = V

    def default_action(self):
        """ Main loop of the actuator.

        Implements the component behaviour
        """
        # update internal states
        self._update_states()

        # Store velocity for Thrustforce calculation
        self.robot_parent.nu = self.nu
        
        # Relative velocity TODO include current
        
        beta = blenderapi.getssr().get('Current_heading')
        NED_current =  (blenderapi.getssr().get('Current_velocity') * numpy.matrix([numpy.cos(beta),numpy.sin(beta),0,0,0,0]).T)
        
        nu_current = self.Rzyx6(self.pose3d.roll,self.pose3d.pitch,self.pose3d.yaw) * NED_current
        self.nu_rel=self.nu - nu_current
        
        
        ###################################################
        # Calculate and apply forces in the vehicle frame #
        ###################################################
        
        localForce = numpy.matrix([0.0 , 0.0 ,0.0 ,0.0 ,0.0 ,0.0]).T
        
        # Restoring moments (forces already taken into account)
        localForce -=self._Restoring_moment(self.g, self.rho, self.mass, self._V, self.r_g, self.r_b, self.pose3d.roll, self.pose3d.pitch)
        
        restoring_force_ned=localForce
        restoring_force_enu=self._to_enu(restoring_force_ned)        

        # Linear Damping
        Ld = self.D_l * self.nu_rel
        localForce -= Ld
        
        # Quadratic damping
        Qd = self.D_q * numpy.multiply(numpy.multiply(self.nu_rel,self.nu_rel),numpy.sign(self.nu_rel))
        localForce -= Qd

        
        # Coreolis MOMENT of added mass TODO investigate if this is correct to include
        localForce -= self._Coreolis_addedmass(self.A, self.nu_rel) * self.nu_rel
        
        # Coriolis of MOMENT rigid body TODO
        localForce -= self._Coreolis_rigid(self.mass, self.nu, self.r_g, self.I_g)*self.nu

        #Forces in SFU (starboard-forward-up)
        localForce = self._to_enu(localForce)
        force  = localForce[0:3].T.tolist()[0]
        torque = localForce[3:6].T.tolist()[0]
        
        #Apply forces
        self.robot.applyExternalForce(force,True)
        self.robot.applyExternalTorque(torque,True)
        
        


        ##########################
        #  Write forces to file  #  TODO Find better way
        ##########################


        #if (self.begin==1):
        #  self.begin=0
        #  self.time_init=morse.core.blenderapi.persistantstorage().time.time

  
        #linDamp=-self.D_l * self.nu_rel
        #quadDamp=-self.D_q * numpy.multiply(numpy.multiply(self.nu_rel,self.nu_rel),numpy.sign(self.nu_rel))
        #Cor_a=-self._Coreolis_addedmass(self.A, self.nu_rel) * self.nu_rel
        #Cor_rb=-self._Coreolis_rigid(self.mass, self.nu, self.r_g, self.I_g)*self.nu

        #time=morse.core.blenderapi.persistantstorage().time.time
        #time_now=time-self.time_init
  
        #self.lin_damping.write('%f  ' % time_now)
        #self.quad_damping.write('%f  ' % time_now)
        #self.coriolis_rb.write('%f  ' % time_now)
        #self.coriolis_a.write('%f  ' % time_now)
        #self.nu_morse.write('%f  ' %time_now)

        #for i in range (0, 6):
        #  linD=linDamp[i, 0]
        #  qD=quadDamp[i, 0]
        #  c_a=Cor_a[i, 0]
        #  c_rb=Cor_rb[i, 0]
        #  vel=self.nu[i, 0]
        #  self.lin_damping.write(str(linD))
        #  self.quad_damping.write(str(qD))
        #  self.coriolis_rb.write(str(c_rb))
        #  self.coriolis_a.write(str(c_a))
        #  self.nu_morse.write(str(vel))
        #  self.coriolis_a.write('  ')
        #  self.coriolis_rb.write('  ')
        #  self.lin_damping.write('  ')
        #  self.quad_damping.write('  ')
        #  self.nu_morse.write('  ')


        #self.coriolis_a.write('\n')
        #self.coriolis_rb.write('\n')
        #self.lin_damping.write('\n')
        #self.quad_damping.write('\n')
        #self.nu_morse.write('\n')


        ###########################################

        
    def _update_states(self):
        self.nu = self._to_ned(numpy.matrix(numpy.concatenate( (self.v, self.w) )).T)
        
        
    def _to_ned(self,vec):
        return numpy.matrix([
        [0,1,0,0,0,0],
        [1,0,0,0,0,0],
        [0,0,-1,0,0,0],
        [0,0,0,0,1,0],
        [0,0,0,1,0,0],
        [0,0,0,0,0,-1]]) * vec
    
    def _to_enu(self,vec):
        return numpy.matrix([
        [ 0.,  1.,  0.,  0.,  0.,  0.],
        [ 1.,  0.,  0.,  0.,  0.,  0.],
        [ 0.,  0., -1.,  0.,  0.,  0.],
        [ 0.,  0.,  0.,  0.,  1.,  0.],
        [ 0.,  0.,  0.,  1.,  0.,  0.],
        [ 0.,  0.,  0.,  0.,  0., -1.]]) * vec


    def _Coreolis_addedmass(self,M_a, nu): 
        
        def Smtrx(r):
            return numpy.matrix([[0,-r[2],r[1]],[r[2],0,-r[0]], [-r[1],r[0],0]])
        
        A11 = M_a[0:3,0:3]
        A12 = M_a[0:3,3:6]
        A21 = M_a[3:6,0:3]
        A22 = M_a[3:6,3:6]
        

        C11 = numpy.zeros((3,3))
        C12 = C11#-1*Smtrx(A11*nu[0:3] + A12*nu[3:6])
        C21 = -1*Smtrx(A11*nu[0:3] + A12*nu[3:6])
        C22 = -1*Smtrx(A21*nu[0:3] + A22*nu[3:6])
        
        #stack and return Coreolis array
        return numpy.hstack((numpy.vstack((C11,C21)),numpy.vstack((C12,C22))))
        
    def _Coreolis_rigid(self, m, nu, r_g, I_g):
        def Smtrx(r):
            return numpy.matrix([[0,-r[2],r[1]],[r[2],0,-r[0]], [-r[1],r[0],0]])
        
        def getInertia_body(I_g, m, rg_skew):
            return I_g-m*rg_skew*rg_skew
        
        I_b=getInertia_body(I_g, m, Smtrx(r_g))

        Crb11 = numpy.zeros((3,3))
        Crb12 = Crb11 #-1*m*Smtrx(nu[0:3]) - m*Smtrx(nu[3:6])*Smtrx(r_g)
        Crb21 = -1*m*Smtrx(nu[0:3]) + m*Smtrx(r_g)*Smtrx(nu[3:6])
        Crb22 = -1*Smtrx(I_b*nu[3:6])
        #stack and return Coreolis array
        return numpy.hstack((numpy.vstack((Crb11,Crb21)),numpy.vstack((Crb12,Crb22))))


    def _Restoring_moment(self, g, rho, m, V, r_g, r_b, pitch, roll):
      W=m*g
      B=rho*g*V
      sin_theta=math.sin(pitch)
      cos_theta=math.cos(pitch)
      sin_roll=math.sin(roll)
      cos_roll=math.cos(roll)

      x_force=0#(W-B)*sin_theta
      y_force=0#-(W-B)*cos_theta*sin_roll
      z_force=0#-(W-B)*cos_theta*cos_roll
      x_torque=-(r_g[1]*W-r_b[1]*B)*cos_theta*cos_roll+(r_g[2]*W-r_b[2]*B)*cos_theta*sin_roll
      y_torque=(r_g[2]*W-r_b[2]*B)*sin_theta+(r_g[0]*W-r_b[0]*B)*cos_theta*cos_roll
      z_torque=-(r_g[0]*W-r_b[0]*B)*cos_theta*sin_roll-(r_g[1]*W-r_b[1]*B)*sin_theta
      return numpy.matrix([[x_force], [y_force], [z_force], [x_torque],[y_torque], [z_torque]])
  
    def Rzyx(self,phi,theta,psi):
        cphi = numpy.cos(phi)
        sphi = numpy.sin(phi)
        cth  = numpy.cos(theta)
        sth  = numpy.sin(theta)
        cpsi = numpy.cos(psi)
        spsi = numpy.sin(psi)
   
        return numpy.matrix([  [cpsi*cth,  -spsi*cphi+cpsi*sth*sphi,  spsi*sphi+cpsi*cphi*sth ],
                            [spsi*cth,  cpsi*cphi+sphi*sth*spsi,   -cpsi*sphi+sth*spsi*cphi],
                            [-sth,      cth*sphi,                  cth*cphi                ] ])
        
    def Rzyx6(self,phi,theta,psi):

        R = numpy.zeros((6,6))
    
        R[0:3,0:3] = self.Rzyx(phi, theta, psi)

        R[3,3] = 1
        R[4,4] = 1
        R[5,5] = 1

        return R
           
                    
        
        
