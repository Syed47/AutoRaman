import numpy as np
from pycromanager import Core

class Camera:
    def __init__(self, core: Core, camera:str = 'AmScope', exposure:int = 15):
        self.core = core
        self.core.set_camera_device(camera)
        self.camera = camera
        self.width = self.core.get_image_width()
        self.height = self.core.get_image_height()
        self.snapped_image = None
        self.set_exposure(exposure)

    def set_exposure(self, val:int = 15):
        self.core.set_exposure(val)

    def set_option(self, option:str = None, value:str = None):
        self.core.set_property(self.camera, option, value)

    def snap_image(self, invert:bool = False):
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

        self.snapped_image = np.max(img) - img if invert else img
        return self.snapped_image
