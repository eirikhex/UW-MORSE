from morse.builder import *
from subseaSintef.builder.actuators import FluidForces
from subseaSintef.builder.actuators import Thrustforces 

class VideoRay(Robot):
    """
    A template robot model for VideoRay, with a motion controller and a pose sensor.
    """
    def __init__(self, name = None, debug = False, Actuators = False, Sensors=False):

        # VideoRay.blend is located in the data/robots directory
        Robot.__init__(self, 'subseaIMR/robots/VideoRay.blend', name)
        self.properties(classpath = "subseaIMR.robots.VideoRay.Videoray")
        
        ###################################
        # Physics Parameters
        ###################################
        self.set_rigid_body()
        self.set_collision_bounds()
        
        self.set_mass(6.1)
        #estimated
        self.Volume = 6.15/(1025.0)
        
        self.M_a = [[2.5028, 0, 0, 0, 0, 0],
                    [0, 7.1401, 0, 0, 0, 0],
                    [0, 0, 8.0125, 0, 0, 0],
                    [0, 0, 0, 0.0283, 0, 0],
                    [0, 0, 0, 0, 0.0371, 0],
                    [0, 0, 0, 0, 0, 0.0395]]
        
        self.M_rb = [[6.1, 0, 0, 0, 0, 0],
                    [0, 6.1, 0, 0, 0, 0],
                    [0, 0, 6.1, 0, 0, 0],
                    [0, 0, 0, 1.5, 0, 0],
                    [0, 0, 0, 0, 1.5, 0],
                    [0, 0, 0, 0, 0, 1.5]]
        
        #Cfd-Damping
        self.D_l = [[ 0.3572, 0, 0, 0, 0, 0],
                    [0,  0.0515, 0, 0, 0, 0],
                    [0, 0,  0.0450, 0, 0, 0],
                    [0, 0, 0,  0.0005, 0, 0],
                    [0, 0, 0, 0, - 0.0005, 0],
                    [0, 0, 0, 0, 0, - 0.0026]]
        
        # Empirical Damping
        self.D_l = [[ 2.3170, 0, 0, 0, 0, 0],
                    [0,  5.0326, 0, 0, 0, 0],
                    [0, 0,  6.6261, 0, 0, 0],
                    [0, 0, 0,  0.0189, 0, 0],
                    [0, 0, 0, 0,  0.0313, 0],
                    [0, 0, 0, 0, 0,  0.0286]]
        
        #CFD-calculated Damping
        self.D_quad =[[ 6.5482, 0, 0, 0, 0, 0],
                      [0, 27.4530, 0, 0, 0, 0],
                      [0, 0, 31.0980, 0, 0, 0],
                      [0, 0, 0,  0.0255, 0, 0],
                      [0, 0, 0, 0,  0.0549, 0],
                      [0, 0, 0, 0, 0,  0.0561]]
        
        # Empirical Damping
        self.D_quad =[[14.473, 0, 0, 0, 0, 0],
                      [0, 31.454, 0, 0, 0, 0],
                      [0, 0, 41.413, 0, 0, 0],
                      [0, 0, 0,  0.033, 0, 0],
                      [0, 0, 0, 0,  0.057, 0],
                      [0, 0, 0, 0, 0,  0.048]]
        
        self.COB = [0, 0, - 0.140 ] 
        
        self.COG = [0, 0, - 0.110 ]
        
        
        
        

        ###################################
        # Actuators
        ###################################
        if Actuators:
            self.fluidForces = FluidForces()
            self.thrusters = Thrustforces()

            self.fluidForces.properties(V=self.Volume)

            self.append(self.thrusters)
            self.append(self.fluidForces)
            
            self.fluidForces.add_parameters(A=self.M_a,rb = self.M_rb, D_l = self.D_l, D_q=self.D_quad, r_g=self.COG, r_b=self.COB)
            
            #Make parameters available for the actuators
            #Thruster limits in "ENU" all but forward estimated
            self.thrusters.add_parameters(thrust_lim = [20.0, 98.1, 20,0,0,98.1*0.05])
            self.thrusters.add_parameters(simple = True)
        



        ###################################
        # Sensors
        ###################################
        if Sensors:
            
            # Camera Sensor
            camera = VideoCamera()
            camera.translate(y=0.2)
            camera.rotate(1.57,0.0,0.0)
            camera.properties(cam_width=800, cam_height=600)
            self.append(camera)

