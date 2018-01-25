from morse.builder import *

class Underwaterrobot(GroundRobot):
    """
    A template robot model for UnderwaterRobot, with a motion controller and a pose sensor.
    """
    def __init__(self, name = None, debug = True):

        # UnderwaterRobot.blend is located in the data/robots directory
        GroundRobot.__init__(self, 'subsea/robots/UnderwaterRobot.blend', name)
        self.properties(classpath = "subsea.robots.UnderwaterRobot.Underwaterrobot")
        
        self.set_rigid_body()
        self.set_mass(20)
        #self._no_gravity = True

        ###################################
        # Actuators
        ###################################


        # (v,w) motion controller
        # Check here the other available actuators:
        # http://www.openrobots.org/morse/doc/stable/components_library.html#actuators
        self.motion = MotionVW()
        self.append(self.motion)

        # Optionally allow to move the robot with the keyboard
        if debug:
            keyboard = Keyboard()
            keyboard.properties(ControlType = 'Position')
            self.append(keyboard)

        ###################################
        # Sensors
        ###################################

        self.pose = Pose()
        self.append(self.pose)

