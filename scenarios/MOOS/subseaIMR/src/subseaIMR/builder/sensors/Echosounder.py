from morse.builder.creator import SensorCreator

class Echosounder(SensorCreator):
    _classpath = "subseaIMR.sensors.Echosounder.Echosounder"
    _blendname = "Echosounder"

    def __init__(self, name=None):
        SensorCreator.__init__(self, name)

