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
            self._camera: ICamera = Camera()
            self._stage: Stage = Stage()
            self._lamp: Lamp = Lamp()
            self._initialized = True 

    @property
    def camera(self) -> ICamera:
        return self._camera

    @camera.setter
    def camera(self, value: ICamera) -> None:
        self._camera = value

    @property
    def stage(self) -> Stage:
        return self._stage

    @stage.setter
    def stage(self, value: Stage) -> None:
        self._stage = value

    @property
    def lamp(self) -> Lamp:
        return self._lamp

    @lamp.setter
    def lamp(self, value: Lamp) -> None:
        self._lamp = value

    def snap_image(self, delay: float = 0.6) -> np.ndarray:
        self.lamp.set_on()
        sleep(delay)

        # Capturing multiple images to ensure stability or correct exposure
        img = None
        for _ in range(4):
            img = self.camera.capture()
            sleep(delay)

        self.lamp.set_off()
        return img

    def auto_focus(self, strategy: Autofocus, start: int, end: int, step: int = 1) -> float:
        self.focus_strategy = strategy(self.camera, self.stage, self.lamp)
        return self.focus_strategy.focus(start, end, step)


# Only exposing microscope variable
microscope = Microscope()
print("microscope started")
__all__ = ['microscope']
