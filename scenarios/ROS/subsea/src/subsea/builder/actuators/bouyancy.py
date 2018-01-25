from morse.builder.creator import ActuatorCreator

class Bouyancy(ActuatorCreator):
    _classpath = "subsea.actuators.bouyancy.Bouyancy"
    def __init__(self, name=None):
        ActuatorCreator.__init__(self, name)

