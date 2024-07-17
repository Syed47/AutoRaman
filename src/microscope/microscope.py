from camera import ICamera, Camera, SpectralCamera
from stage import Stage
from lamp import Lamp
from autofocus import Autofocus
from time import sleep
import numpy as np

class Microscope:

    def __init__(self):
        self.camera:ICamera = Camera()
        self.stage:Stage = Stage()
        self.lamp:Lamp = Lamp()

    def snap_image(self, delay=0.6):
        self.lamp.set_on()
        sleep(delay)
        img = self.camera.capture()
        sleep(delay)
        img = self.camera.capture()
        sleep(delay)
        img = self.camera.capture()
        sleep(delay)
        img = self.camera.capture()
        sleep(delay)
        self.lamp.set_off()
        return img

        
    def auto_focus(self, strategy:Autofocus, start, end, step=1):
        self.focus_strategy = strategy(self.camera, self.stage, self.lamp)
        return self.focus_strategy.focus(start, end, step)



