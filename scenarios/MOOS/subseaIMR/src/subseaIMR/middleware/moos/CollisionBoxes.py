import logging; logger = logging.getLogger("morse." + __name__)
import re
import ast
import numpy as np
from subseaIMR.middleware.moos.abstract_moos import AbstractMOOS

class CollisionReader(AbstractMOOS):
    """ Read motion commands and update local data. """

    def initialize(self):
        AbstractMOOS.initialize(self)

        self.comms.set_on_connect_callback( self.register_variables )
        print("initialized") 
    
    def register_variables(self):
        self.register("COLLISIONS")
        return(True)
    
    def default(self, ci='unused'):
        current_time = self.time()
        # get latest mail from the MOOS comm client
        messages = self.comms.fetch()
        new_information = False
        for message in messages:
            # look for command messages
            if (message.key() == "COLLISIONS") and (message.is_string()):
                print(message.string())
                collisions = np.array(self.string_to_matrix(message.string())).reshape(-1).tolist()
                self.data['collision_list'] = collisions
                print(collisions)
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

        

        
        
        
        
        
        
        