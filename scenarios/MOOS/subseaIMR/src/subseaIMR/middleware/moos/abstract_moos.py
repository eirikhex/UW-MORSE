import logging; logger = logging.getLogger("morse.moos")
import pymoos

from morse.middleware import AbstractDatastream
from morse.core import blenderapi


class AbstractMOOS(AbstractDatastream):
    
    """ Base class for all MOOS Publishers and Subscribers """
    # used to generate documentation, TODO fill in subclasses
    _type_name = "db entries"
    _type_url = ""
    _moosapps = {}
    _save_messages = {}

    def initialize(self):
        """ Initialize the MOOS app. """
        logger.info("MOOS datastream initialize %s"%self)
        
        
        self.moos_host = self.kwargs.get('moos_host', 'localhost')
        self.moos_port = self.kwargs.get('moos_port', 9000)
        self.moos_name = self.kwargs.get('moos_name', self.component_name)
        
        
        '''
        key = (self.moos_host, self.moos_port)

        if not key in AbstractMOOS._moosapps:
            AbstractMOOS._save_messages[key] = []
            AbstractMOOS._moosapps[key] = pymoos.MOOSCommClient.MOOSApp()
            AbstractMOOS._moosapps[key].Run(self.moos_host,
                                            self.moos_port,
                                            "uMorse", 
                                            self.moos_freq)
            logger.info("\tdatastream: host=%s:port=%d (freq: %.2fHz)"
                %(self.moos_host, self.moos_port, self.moos_freq))
            logger.info("\tnew interface initialized")
            '''

        # all instance share the same static MOOSApp according to host and port
        self.comms = pymoos.comms()
        
        self.comms.run(self.moos_host,self.moos_port,self.moos_name)
        self.time = pymoos.time
        
    
    def register(self,var,frequency = 0):
        self.comms.register(var,frequency)
        
    def notify(self,var,val,time=pymoos.time()):
        self.comms.notify(var,val,time)
    



    def finalize(self):
        """ Kill the morse MOOS app."""
        self.comms.close(True)


'''
class StringPublisher(AbstractMOOS):
    """ Publish a string containing a printable representation of the
    local data. """

    def default(self, ci='unused'):
        logger.debug("Posting message to the MOOS database.")
        current_time = blenderapi.persistantstorage().time.time
        #iterate through all objects of the component_instance and post the data
        for variable, data in self.data.items():
            name = "%s_%s" % (self.component_name, variable)
            logger.debug("name: %s, type: %s, data: %s"%
                                (name, type(data), str(data)))
            self.m.Notify(name, str(data), current_time)
            


class StringReader(AbstractMOOS):
    """ Log messages. """

    def default(self, ci='unused'):
        # get latest mail from the MOOS comm client
        messages = self.m.FetchRecentMail()

        # log messages
        for message in messages:
            logger.info("message: %s" % str(message))
'''