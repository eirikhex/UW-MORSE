import logging; logger = logging.getLogger("morse." + __name__)

import morse.core.actuator

from morse.core.services import service, async_service, interruptible
from morse.core import status, blenderapi
from morse.helpers.components import add_data, add_property

class Bouyancy(morse.core.actuator.Actuator):
    """Write here the general documentation of your actuator.
    It will appear in the generated online documentation.
    """
    _name = "Bouyancy"
    _short_desc = "Adds bouyancy to an underwater robot"

    # define here the data fields required by your actuator
    # format is: field name, initial value, type, description
    add_data('rho', 1025, 'float', 'Fluid density [kg/m3]')
    add_data('V',0.0,'float', 'Volume of robot')

    def __init__(self, obj, parent=None):
        logger.info("%s initialization" % obj.name)
        # Call the constructor of the parent class
        morse.core.actuator.Actuator.__init__(self, obj, parent)
        self.do_once = False
        # Do here actuator specific initializations

        logger.info('Component initialized')

    

    def default_action(self):
        """ Main loop of the actuator.

        Implements the component behaviour
        """
        robot = self.robot_parent
        
        force = (robot.bge_object.mass * -9.81)
        #robot.bge_object.applyForce([0.0, 0.0,  force], False)
        
        force2 = (robot.bge_object.mass * blenderapi.game_settings().physics_gravity)
        robot.bge_object.applyForce([0.0, 0.0,  force2], False)
        
        keyboard = blenderapi.keyboard()
        is_actived = blenderapi.input_active()
        
        if keyboard.events[blenderapi.ZKEY] == is_actived:
            self.local_data['V'] = self.local_data['V']+1.0
            print(self.local_data['V'])
            
        if keyboard.events[blenderapi.XKEY] == is_actived:
            self.local_data['V'] = self.local_data['V']-1.0
            print(self.local_data['V'])
            
        force3 = self.local_data['V']
        #robot.bge_object.applyForce([0.0, 0.0,  force3], False)
        
        
        
        
        if not self.do_once:
            print(robot.bge_object.mass)
            print(robot.bge_object.getPropertyNames())
            print(blenderapi.game_settings().physics_gravity)
            #print(robot.bge_object.getLinearVelocity())
            self.do_once = True
