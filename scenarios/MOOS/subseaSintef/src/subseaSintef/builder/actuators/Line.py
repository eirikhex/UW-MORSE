from morse.builder.creator import ActuatorCreator

class Line(ActuatorCreator):
    _classpath = "subseaSintef.actuators.Line.Line"
    _blendname = "Line"

    def __init__(self, name=None):
        ActuatorCreator.__init__(self, name)

