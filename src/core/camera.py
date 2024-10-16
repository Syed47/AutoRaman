import numpy as np
from abc import ABC, abstractmethod
from core.controller import controller

import matplotlib.pyplot as plt
import os

class Camera(ABC):
    def __init__(self, camera:str):
        self.controller = controller
        self.camera = camera
        self.snapped_image = None
        self.controller.set_camera_device(self.camera)
        self.width = self.controller.get_image_width()
        self.height = self.controller.get_image_height()
        os.makedirs(f"Autofocus/snaps", exist_ok=True)

    def set_option(self, option:str = None, value:str = None):
        self.controller.set_property(self.camera, option, value)

    def get_property(self, option:str = None):
        self.controller.get_property(self.camera, option)

    def set_exposure(self, val:int = 15):
        self.controller.set_exposure(val)

    def set_camera(self, camera:str):
        self.camera = camera
        self.controller.set_camera_device(self.camera)

    @abstractmethod
    def capture(self) -> np.array:
        pass


class CCDCamera(Camera):
    def __init__(self, camera:str='AmScope', exposure:int=15):
        super().__init__(camera)
        self.set_exposure(exposure)
       
    def capture(self) -> np.array:
        self.controller.snap_image()
        img = self.controller.get_image()
        byte_depth = self.controller.get_bytes_per_pixel()

        if byte_depth == 1:
            img = np.reshape(img, (self.height, self.width, 1)).astype(np.uint8)
        elif byte_depth == 2:
            img = np.reshape(img, (self.height, self.width, 2)).astype(np.uint16)
        elif byte_depth == 3:
            img = np.reshape(img, (self.height, self.width, 3)).astype(np.uint16)
        elif byte_depth == 4:
            img = np.reshape(img, (self.height, self.width, 4)).astype(np.uint16)
        else:
            raise ValueError(f'Invalid byte depth: {byte_depth}')
        
        self.snapped_image = img

        return self.snapped_image


class SpectralCamera(Camera):
    def __init__(self, camera:str='Andor', exposure:int=1000):
        super().__init__(camera)
        self.set_exposure(exposure)
    
    def capture(self) -> np.array:
        self.controller.snap_image()
        img = self.controller.get_image()
        return np.reshape(img, (self.height, self.width))
