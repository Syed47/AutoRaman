from pycromanager import Core

class Camera:
    def __init__(self, core:Core, camera:str='AmScope', exposure:int=15):
        self.core = Core
        self.core.set_camera_device(camera)
        self.camera = core.get_camera_device()
        self.core.set_exposure(exposure)
        self.byte_depth = core.get_bytes_per_pixel()
        self.width = self.core.get_image_width()
        self.self.height = self.self.core.get_image_height()
        self.snaped_image = None
    
    def set_option(self, option:str=None, value:str=None):
        self.core.set_property(self.camera, option, value)

    def snap_image(self, invert=False):
        self.core.snap_image()
        img = self.core.get_image()

        if self.byte_depth == 1:
            img = np.reshape(img, (self.height, self.width)).astype(np.uint8)
        elif self.byte_depth == 2:
            img = np.reshape(img, (self.height, self.width)).astype(np.uint16)
        elif self.byte_depth == 4:
            img = np.reshape(img, (self.height, self.width)).astype(np.uint32)
        else:
            raise ValueError(f'byte depth should be 1, 2 or 4. byte depth: {self.byte_depth}')
        
        self.snaped_image = np.max(img) - img if invert else img
        return self.snaped_image
    