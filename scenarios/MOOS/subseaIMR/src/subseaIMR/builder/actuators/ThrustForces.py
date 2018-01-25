from morse.builder.creator import ActuatorCreator
from morse.builder import bpymorse
import json


class Thrustforces(ActuatorCreator):
    _classpath = "subseaIMR.actuators.ThrustForces.Thrustforces"
    _blendname = "ThrustForces"

    def __init__(self, name=None):
        ActuatorCreator.__init__(self, name)
        self.parameters = {}

    def after_renaming(self):
        
        def dict_to_file(dic, text):
            text.clear()
            text.write('import json \np = json.loads("'+ json.dumps(dic)+'")')
            
            
        if not 'parameters.py' in bpymorse.get_texts().keys():
            bpymorse.new_text()
            bpymorse.get_last_text().name = 'parameters.py'
            dict_to_file({},bpymorse.get_text('parameters.py'))
        
        #text = bpymorse.get_text('parameters.py')
        # load the parameters dictionary from the file    
        #parameters = json.loads(text.as_string())
        from parameters import p 
        
        # set the Object dictionary in the parameters dictionary
        p[self.name] = self.parameters
        
        dict_to_file(p, bpymorse.get_text('parameters.py'))
        
        
        
    def add_parameters(self,**parameters):
        self.parameters.update(parameters)
