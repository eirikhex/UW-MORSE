import logging; logger = logging.getLogger("morse." + __name__)
import morse.core.actuator
from collections import deque

from morse.core.blenderapi import render
from morse.core.services import service, async_service, interruptible
from morse.core import status
from morse.helpers.components import add_data, add_property

class Line(morse.core.actuator.Actuator):
    """Write here the general documentation of your actuator.
    It will appear in the generated online documentation.
    """
    _name = "Line"
    _short_desc = "Draws a line after the robot in 3d space"

    # define here the data fields required by your actuator
    # format is: field name, initial value, type, description
    add_data('counter', 0, 'int', 'A dummy counter, for testing purposes')

    def __init__(self, obj, parent=None):
        logger.info("%s initialization" % obj.name)
        # Call the constructor of the parent class
        morse.core.actuator.Actuator.__init__(self, obj, parent)

        # Do here actuator specific initializations
        
        self.positions = deque()
        self.pose3d=self.robot_parent.position_3d
        
        self.queue_length = 5000
        self. color = [0,0,1]

        logger.info('Component initialized')
        
    def update_queue(self):
        if len(self.positions) > self.queue_length:
            self.positions.popleft()
            
        self.positions.append([self.pose3d.x,self.pose3d.y,self.pose3d.z])
        
    def draw_line(self):
        for i in range(0,len(self.positions)-2):
            start = self.positions[i]
            end   = self.positions[i+1]
            
            render().drawLine(start,end,self.color)
            



    def default_action(self):
        """ Main loop of the actuator.

        Implements the component behaviour
        """
        # save current position and update queue
        self.update_queue()
        self.draw_line()
        # draw lines between all positions in queue
        

