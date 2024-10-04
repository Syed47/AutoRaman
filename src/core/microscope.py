from core.camera import ICamera, Camera, SpectralCamera
from core.stage import Stage
from core.lamp import Lamp
from core.autofocus import Autofocus
from time import sleep
import numpy as np

class Microscope:
    _instance = None 

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(Microscope, cls).__new__(cls)
        return cls._instance

    def __init__(self):
        if not hasattr(self, '_initialized'):
            self.camera: ICamera = Camera()
            self.stage: Stage = Stage()
            self.lamp: Lamp = Lamp()
            self.focus_strategy = None
            self._initialized = True 

    def snap_image(self):
        img = self.camera.capture()
        sleep(1)
        return img

    def move_stage(self, x=0, y=0, z=0):
        self.stage.moveby(x, y, z)

    def auto_focus(self, strategy: Autofocus, start: int, end: int, step: int = 1, callback=None) -> float:
        self.focus_strategy = strategy(self.camera, self.stage, self.lamp)
        return self.focus_strategy.focus(start, end, step, callback)


# Only exposing microscope variable
microscope = Microscope()
__all__ = ['microscope']
