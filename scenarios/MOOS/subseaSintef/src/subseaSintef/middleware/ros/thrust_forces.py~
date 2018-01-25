import logging; logger = logging.getLogger("morse." + __name__)
import roslib; roslib.load_manifest('std_msgs')
from std_msgs.msg import Float32MultiArray
from morse.middleware.ros import ROSSubscriber
import numpy

class Float32MultiArraySubscriber(ROSSubscriber):
    """ Subscribe to a Float32MultiArray message and set the RPM for the thrust sensor"""
    ros_class = Float32MultiArray
    
    def update(self, msg):
        RPM1=msg.data[0]
        RPM2=msg.data[1]
        RPM3=msg.data[2]
        RPM4=msg.data[3]
        RPM5=msg.data[4]
      
        self.data['RPM']=numpy.matrix([RPM1, RPM2, RPM3, RPM4, RPM5])
        
        logger.debug("Setting RPM: [%s, %s, %s, %s, %s ]"%
                     (RPM1, RPM2,RPM3, RPM4, RPM5,))
    


