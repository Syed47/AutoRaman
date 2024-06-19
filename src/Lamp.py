from pycromanager import Core

class Lamp:
    def __init__(self, core:Core):
        self.core = core
    
    def set_on(self):
        self.core.set_property("TransmittedLamp", "Label", "On")
    
    def set_off(self):
        self.core.set_property("TransmittedLamp", "Label", "Off")
