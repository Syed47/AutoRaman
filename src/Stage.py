from pycromanager import Core

class Stage:
    def __init__(self, core:Core):
        self.core = core
        self.vertical = self.core.get_focus_device()
        self.horizontal = self.core.get_xy_stage_device()
        self.x = self.core.get_x_position(self.horizontal)
        self.x = self.core.get_y_position(self.horizontal)
        self.z = self.core.get_position(self.vertical)
    
    def move(self, x=None, y=None, z=None):
        self.x = self.core.get_x_position(self.horizontal) if x == None else x
        self.y = self.core.get_y_position(self.horizontal) if y == None else y
        self.z = self.core.get_position(self.vertical) if z == None else z
        self.core.set_xy_position(self.horizontal, self.x, self.y)
        self.core.set_position(self.vertical, self.z)

