import pymoos
import numpy as np
import cv2


def register_variables():
    comms.register('Video',0.0)
    comms.register("cRPM1",0.0)
    comms.register("cRPM2",0.0)
    comms.register("cRPM3",0.0)
    comms.register("cRPM4",0.0)
    comms.register("desiredThrust",0.0)
    return True

comms = pymoos.comms()
        
comms.run('localhost',9000, 'Recorder')
time = pymoos.time

comms.set_on_connect_callback(register_variables )

while(True):
    messages = comms.fetch()
    for message in messages:
        print(message)
        print(pymoos.__file__)
        print(message.key())
            # look for command messages
        if (message.key() == "Video") :
            image = bytes()
            image = message.binary_data()
            print(len(image))
            nparr = np.frombuffer(image, np.uint8).reshape( 1280, 720, 4 )
            cv2.imshow('video',nparr)
            cv2.waitKey(50)