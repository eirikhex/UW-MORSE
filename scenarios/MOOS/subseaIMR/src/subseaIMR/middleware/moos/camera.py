import logging; logger = logging.getLogger("morse." + __name__)
import numpy as np
import pickle
import copy
import cv2
from PIL import Image
from subseaIMR.middleware.moos.abstract_moos import AbstractMOOS

import gi
gi.require_version('Gst', '1.0')
from gi.repository import GObject, Gst


class CameraNotifyer(AbstractMOOS):
    
    def initialize(self):
        AbstractMOOS.initialize(self)

        self.show = False
        self.movie = []
        self.bg_color = [56, 53, 70, 255]


    def default(self, ci = 'unused'):
        cur_time = self.time()
        #get ImageRender Object
        image = self.data['image']
        x,y = image.size
        img1 = np.reshape(image, (y,x,4))
        img = Image.fromarray(img1,'RGBA')
        if self.show:
            self.show = False;
            img.show()
        #print(cv2.__file__)
        #opencv_image = np.array(img)
        #opencv_image = opencv_image[:, :, ::-1].copy() 
        #print(opencv_image)
        #cv2.imshow('video',opencv_image)
        #cv2.waitKey(1)
        self.comms.notify_binary('Video',bytes(image),self.time())
        """
        GObject.threads_init()
        Gst.init(None)
        
        appsrc = Gst.ElementFactory.make("appsrc", "appsrc")
        filesink = Gst.ElementFactory.make("filesink", "filesink")
        filesink.set_property("location", "test.dat")

        pipeline = Gst.Pipeline()
        pipeline.add(appsrc)
        pipeline.add(filesink)
        appsrc.link(filesink)
        pipeline.set_state(Gst.State.PLAYING)
        
        data = bytes(image)

        buf = Gst.Buffer.new_allocate(None, len(data), None)
        appsrc.emit("push-buffer", buf)

        pipeline.send_event(Gst.Event.new_eos())
        """
        
        #self.movie.append(img1)
        #f = open('move.p','wb')
        #pickle.dump(self.movie,f)
        #f.close()
        

        
        
        #img2 = cv2.cvtColor(img1, cv2.COLOR_RGBA2BGRA) #Red and blue need swapped for opencv
        #img2 = np.flipud(img2) #BGE always gives upside down results. This flips it.
        
        #pickle.dump(img2,open('img2.p','wb'))
            #nparr = np.fromstring(image, np.float32).reshape( self.component_instance.image_height, self.component_instance.image_width, 4 )
        #print(image)
        #
        #image.reshape(self.component_instance.image_height, self.component_instance.image_width, 4)
        
        #cv2.imshow('Camera',nparr)
        #cv2.waitKey(50)
