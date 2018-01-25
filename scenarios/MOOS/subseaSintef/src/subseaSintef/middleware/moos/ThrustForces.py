import logging; logger = logging.getLogger("morse." + __name__)
import pymoos
import re
import ast
import numpy as np
from subseaSintef.middleware.moos.abstract_moos import AbstractMOOS

class ThrustForcesReader(AbstractMOOS):
    """ Read motion commands and update local data. """

    def initialize(self):
        AbstractMOOS.initialize(self)

        self.comms.set_on_connect_callback( self.register_variables )
        print("initialized") 
    
    def register_variables(self):
        self.register("cRPM1")
        self.register("cRPM2")
        self.register("cRPM3")
        self.register("cRPM4")
        self.register("cRPM5")
        self.register("desiredThrust")
        return(True)
    
    def default(self, ci='unused'):
        current_time = pymoos.time()
        # get latest mail from the MOOS comm client
        messages = self.comms.fetch()
        new_information = False

        for message in messages:
            # look for command messages
            if (message.key() == "cRPM1") and (message.is_double()):
                self.data['RPM'][0,0] = message.double() # command linear velocity [m/s]
                new_information = True
            elif  (message.key() == "cRPM2") and (message.is_double()):
                self.data['RPM'][0,1] = message.double() # command angular velocity [m/s]
                new_information = True
            elif  (message.key() == "cRPM3") and (message.is_double()):
                self.data['RPM'][0,2] = message.double() # command steer angle [deg]
                new_information = True
            elif  (message.key() == "cRPM4") and (message.is_double()):
                self.data['RPM'][0,3] = message.double() # command engine force
                new_information = True
            elif  (message.key() == "cRPM5") and (message.is_double()):
                self.data['RPM'][0,4] = message.double() # command angular velocity [m/s]
                new_information = True
            elif (message.key() == "desiredThrust") and (message.is_string()):
                thrust = np.matrix(self.string_to_matrix(message.string()))
                self.data['ThrustForce'] = thrust
                new_information = True

        return new_information
    
    def parse_matrix(self,str):
        # array to save the vector
        matrix = []
        
        # strip white spaces and brackets
        str = ''.join(re.split("[\ \[\]]",str))
        rows = str.split(";")
        #TODO: Error handling
        for row in rows:
            numbers = row.split(",")
            row_vec = []
            for number in numbers:
                row_vec.append(float(number))
            
            matrix.append(row_vec)
        
        return matrix;
    
    def matrix_to_string(self, mat):
        ''' Format numpy matrix to matlab matrix format
        '''
        str = "["+ np.array2string(np.array(mat),separator=",").replace(",\n",";").replace("[","").replace("]","") +"]"
        return str
        
    def string_to_matrix(self,string):
        ''' Make numpy matrix from matlab matrix style string
        '''
        try:
            string = "[" +string.replace(";","],[").replace(" ","") + "]"
            matrix = np.matrix(ast.literal_eval(string))
            return matrix
        except:
            return None

        

        
        
        
        
        
        
        