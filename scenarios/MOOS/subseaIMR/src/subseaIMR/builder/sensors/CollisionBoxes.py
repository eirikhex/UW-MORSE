from morse.builder.creator import SensorCreator
from morse.builder.blenderobjects import *
import numpy as np

class CollisionBoxes(SensorCreator):
    _classpath = "subseaIMR.sensors.CollisionBoxes.CollisionBoxes"
    _blendname = "CollisionBoxes"

    def __init__(self, name=None):
        SensorCreator.__init__(self, name)
        
        self.overall_box_size = [5.0, 5.0, 5.0]
        self.octree_level = 2
        
        number_of_boxes_in_one_dim = np.power(2,self.octree_level)
        self.box_size = np.divide(self.overall_box_size , number_of_boxes_in_one_dim).tolist()
        self.make_boxes()
        
    def make_boxes(self):
        boxes = self.make_box_dict()
        box_scale_val = np.multiply([0.5, 0.5, 0.5], self.box_size).tolist()
        
        
        for key, value in boxes.items():
            name = "CollisionCube_" + str(key)
            mesh = Cube(name)
            mesh.name = name
            mesh.scale = tuple(np.array(box_scale_val).reshape(-1))
            #mesh.scale = (0.5, 0.5, 0.5)
            mesh.color(.0, .9, .6)
            mesh.location = tuple(np.array(value).reshape(-1))
            #mesh.location = (0.0, -0.5, 0.0) 
            mesh._bpy_object.active_material.alpha = 0.5
            mesh._bpy_object.active_material.use_transparency = True
            mesh._bpy_object.active_material.name = "Mat_" + name
            mesh._bpy_object.active_material.type = 'VOLUME'

            self.append(mesh)
    
    
    def make_box_dict(self):
        vehicle = {}
        
        # Layer 0
        vehicle[11] = np.multiply(self.box_size, [-1.5, -1.5,  -1.5]).tolist()
        vehicle[13] = np.multiply(self.box_size, [-0.5, -1.5,  -1.5]).tolist()
        vehicle[15] = np.multiply(self.box_size, [-1.5, -0.5,  -1.5]).tolist()
        vehicle[17] = np.multiply(self.box_size, [-0.5, -0.5,  -1.5]).tolist()

        vehicle[31] = np.multiply(self.box_size, [ 0.5, -1.5,  -1.5]).tolist()
        vehicle[33] = np.multiply(self.box_size, [ 1.5, -1.5,  -1.5]).tolist()
        vehicle[35] = np.multiply(self.box_size, [ 0.5, -0.5,  -1.5]).tolist()
        vehicle[37] = np.multiply(self.box_size, [ 1.5, -0.5,  -1.5]).tolist()
            
        vehicle[51] = np.multiply(self.box_size, [-1.5,  0.5,  -1.5]).tolist()
        vehicle[53] = np.multiply(self.box_size, [-0.5,  0.5,  -1.5]).tolist()
        vehicle[55] = np.multiply(self.box_size, [-1.5,  1.5,  -1.5]).tolist()
        vehicle[57] = np.multiply(self.box_size, [-0.5,  1.5,  -1.5]).tolist()
            
        vehicle[71] = np.multiply(self.box_size, [ 0.5,  0.5,  -1.5]).tolist()
        vehicle[73] = np.multiply(self.box_size, [ 1.5,  0.5,  -1.5]).tolist()
        vehicle[75] = np.multiply(self.box_size, [ 0.5,  1.5,  -1.5]).tolist()
        vehicle[77] = np.multiply(self.box_size, [ 1.5,  1.5,  -1.5]).tolist()
        
        # Layer 1
        vehicle[10] = np.multiply(self.box_size, [-1.5, -1.5,  -0.5]).tolist()
        vehicle[12] = np.multiply(self.box_size, [-0.5, -1.5,  -0.5]).tolist()
        vehicle[14] = np.multiply(self.box_size, [-1.5, -0.5,  -0.5]).tolist()
        vehicle[16] = np.multiply(self.box_size, [-0.5, -0.5,  -0.5]).tolist()
            
        vehicle[30] = np.multiply(self.box_size, [ 0.5, -1.5,  -0.5]).tolist()
        vehicle[32] = np.multiply(self.box_size, [ 1.5, -1.5,  -0.5]).tolist()
        vehicle[34] = np.multiply(self.box_size, [ 0.5, -0.5,  -0.5]).tolist()
        vehicle[36] = np.multiply(self.box_size, [ 1.5, -0.5,  -0.5]).tolist()
        
        vehicle[50] = np.multiply(self.box_size, [-1.5,  0.5,  -0.5]).tolist()
        vehicle[52] = np.multiply(self.box_size, [-0.5,  0.5,  -0.5]).tolist()
        vehicle[54] = np.multiply(self.box_size, [-1.5,  1.5,  -0.5]).tolist()
        vehicle[56] = np.multiply(self.box_size, [-0.5,  1.5,  -0.5]).tolist()
    
        vehicle[70] = np.multiply(self.box_size, [ 0.5,  0.5,  -0.5]).tolist()
        vehicle[72] = np.multiply(self.box_size, [ 1.5,  0.5,  -0.5]).tolist()
        vehicle[74] = np.multiply(self.box_size, [ 0.5,  1.5,  -0.5]).tolist()
        vehicle[76] = np.multiply(self.box_size, [ 1.5,  1.5,  -0.5]).tolist()
    
        # Layer 2
        vehicle[1] =  np.multiply(self.box_size, [-1.5, -1.5,  0.5]).tolist()
        vehicle[3] =  np.multiply(self.box_size, [-0.5, -1.5,  0.5]).tolist()
        vehicle[5] =  np.multiply(self.box_size, [-1.5, -0.5,  0.5]).tolist()
        vehicle[7] =  np.multiply(self.box_size, [-0.5, -0.5,  0.5]).tolist()
        
        vehicle[21] = np.multiply(self.box_size, [ 0.5, -1.5,  0.5]).tolist()
        vehicle[23] = np.multiply(self.box_size, [ 1.5, -1.5,  0.5]).tolist()
        vehicle[25] = np.multiply(self.box_size, [ 0.5, -0.5,  0.5]).tolist()
        vehicle[27] = np.multiply(self.box_size, [ 1.5, -0.5,  0.5]).tolist()
        
        vehicle[41] = np.multiply(self.box_size, [-1.5,  0.5,  0.5]).tolist()
        vehicle[43] = np.multiply(self.box_size, [-0.5,  0.5,  0.5]).tolist()
        vehicle[45] = np.multiply(self.box_size, [-1.5,  1.5,  0.5]).tolist()
        vehicle[47] = np.multiply(self.box_size, [-0.5,  1.5,  0.5]).tolist()
        
        vehicle[61] = np.multiply(self.box_size, [ 0.5,  0.5,  0.5]).tolist()
        vehicle[63] = np.multiply(self.box_size, [ 1.5,  0.5,  0.5]).tolist()
        vehicle[65] = np.multiply(self.box_size, [ 0.5,  1.5,  0.5]).tolist()
        vehicle[67] = np.multiply(self.box_size, [ 1.5,  1.5,  0.5]).tolist()
        
        # Layer 3
        vehicle[0]  = np.multiply(self.box_size, [-1.5, -1.5,  1.5]).tolist()
        vehicle[2]  = np.multiply(self.box_size, [-0.5, -1.5,  1.5]).tolist()
        vehicle[4]  = np.multiply(self.box_size, [-1.5, -0.5,  1.5]).tolist()
        vehicle[6]  = np.multiply(self.box_size, [-0.5, -0.5,  1.5]).tolist()
        
        vehicle[20] = np.multiply(self.box_size, [ 0.5, -1.5,  1.5]).tolist()
        vehicle[22] = np.multiply(self.box_size, [ 1.5, -1.5,  1.5]).tolist()
        vehicle[24] = np.multiply(self.box_size, [ 0.5, -0.5,  1.5]).tolist()
        vehicle[26] = np.multiply(self.box_size, [ 1.5, -0.5,  1.5]).tolist()
        
        vehicle[40] = np.multiply(self.box_size, [ -1.5, 0.5,  1.5]).tolist()
        vehicle[42] = np.multiply(self.box_size, [ -0.5, 0.5,  1.5]).tolist()
        vehicle[44] = np.multiply(self.box_size, [ -1.5, 1.5,  1.5]).tolist()
        vehicle[46] = np.multiply(self.box_size, [ -0.5, 1.5,  1.5]).tolist()
        
        vehicle[60] = np.multiply(self.box_size, [ 0.5,  0.5,  1.5]).tolist()
        vehicle[62] = np.multiply(self.box_size, [ 1.5,  0.5,  1.5]).tolist()
        vehicle[64] = np.multiply(self.box_size, [ 0.5,  1.5,  1.5]).tolist()
        vehicle[66] = np.multiply(self.box_size, [ 1.5,  1.5,  1.5]).tolist()
        
        return(vehicle)

