import logging; logger = logging.getLogger("morse." + __name__)
import pymoos.MOOSCommClient
from morse.middleware.moos import AbstractMOOS

class ThrustForcesReader(AbstractMOOS):
    """ Read motion commands and update local data. """

    def initialize(self):
        AbstractMOOS.initialize(self)
        self.RegisterVariables()
        OK = self.m.SetOnConnectCallBack( self.RegisterVariables() ) #TODO: Find out why the connect callback don't work
        print(self.m.onMailCallBack)
    def RegisterVariables(self):
        self.m.Register("cRPM1")
        self.m.Register("cRPM2")
        self.m.Register("cRPM3")
        self.m.Register("cRPM4")
        self.m.Register("cRPM5")
    
    def default(self, ci='unused'):
        current_time = pymoos.MOOSCommClient.MOOSTime()
        # get latest mail from the MOOS comm client
        messages = self.getRecentMail()

        new_information = False

        for message in messages:
            # look for command messages
            if (message.GetKey() == "cRPM1") and (message.IsDouble()):
                self.data['RPM'][0,0] = message.GetDouble() # command linear velocity [m/s]
                new_information = True
            elif  (message.GetKey() == "cRPM2") and (message.IsDouble()):
                self.data['RPM'][0,1] = message.GetDouble() # command angular velocity [m/s]
                new_information = True
            elif  (message.GetKey() == "cRPM3") and (message.IsDouble()):
                self.data['RPM'][0,2] = message.GetDouble() # command steer angle [deg]
                new_information = True
            elif  (message.GetKey() == "cRPM4") and (message.IsDouble()):
                self.data['RPM'][0,3] = message.GetDouble() # command engine force
                new_information = True
            elif  (message.GetKey() == "cRPM5") and (message.IsDouble()):
                self.data['RPM'][0,4] = message.GetDouble() # command angular velocity [m/s]
                new_information = True

        return new_information
