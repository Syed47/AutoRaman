import numpy as np
from abc import ABC, abstractmethod
from pycromanager import Core



class ICamera(ABC):
    def __init__(self, core:Core, camera:str = 'AmScope'):
        self.core = core
        self.camera = camera
        self.core.set_camera_device(self.camera)

    def set_option(self, option:str=None, value:str=None):
        self.core.set_property(self.camera, option, value)

    def set_exposure(self, val:int = 15):
        self.core.set_exposure(val)

    @abstractmethod
    def capture(self) -> np.array:
        pass

class SpectralCamera(ICamera):
    def __init__(self, core:Core, camera:str = 'AmScope'):
        super().__init__(self, core, camera)
    
    def capture(self) -> np.array:
        pass


class Camera(ICamera):
    def __init__(self, core:Core, camera:str = 'AmScope', exposure:int = 15):
        super().__init__(self)
        self.width = self.core.get_image_width()
        self.height = self.core.get_image_height()
        self.snapped_image = None
        self.set_exposure(exposure)

    def capture(self) -> np.array:
        self.core.snap_image()
        img = self.core.get_image()

        byte_depth = self.core.get_bytes_per_pixel()

        if byte_depth == 1:
            img = np.reshape(img, (self.height, self.width)).astype(np.uint8)
        elif byte_depth == 2:
            img = np.reshape(img, (self.height, self.width)).astype(np.uint16)
        elif byte_depth == 3 or byte_depth == 4:
            img = np.reshape(img, (self.height, self.width)).astype(np.uint32)
        else:
            raise ValueError(f'Invalid byte depth: {byte_depth}')
        
        self.snap_image = img

        return self.snapped_image
