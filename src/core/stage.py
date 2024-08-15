from core.controller import controller

class Stage:
    def __init__(self):
        self.controller = controller
        self.focus_device = self.controller.get_focus_device()
        self.xy_stage_device = self.controller.getxy_stage_device()
        self._x = self.controller.get_x_position(self.xy_stage_device)
        self._y = self.controller.get_y_position(self.xy_stage_device)
        self._z = self.controller.get_position(self.focus_device)
    
    def move(self, x=None, y=None, z=None):
        if x is not None:
            self._x = x
        if y is not None:
            self._y = y
        if z is not None:
            self._z = z
        
        self.controller.set_xy_position(self.xy_stage_device, self._x, self._y)
        self.controller.set_position(self.focus_device, self._z)

    def moveby(self, x=None, y=None, z=None):
        if x is not None:
            self._x += x
        if y is not None:
            self._y += y
        if z is not None:
            self._z += z
        
        self.controller.set_xy_position(self.xy_stage_device, self._x, self._y)
        self.controller.set_position(self.focus_device, self._z)
    
    @property
    def x(self):
        self._x = self.controller.get_x_position(self.xy_stage_device)
        return self._x
    
    @property
    def y(self):
        self._y = self.controller.get_y_position(self.xy_stage_device)
        return self._y
    
    @property
    def z(self):
        self._z = self.controller.get_position(self.focus_device)
        return self._z

