import tifffile as tiff
import numpy as np
from abc import ABC, abstractmethod
from pycromanager import Core

from Lamp import Lamp
from Stage import Stage
from Camera import Camera

class Autofocus(ABC):
    @abstractmethod
    def focus(self):
        pass

class Raman(Autofocus):
    def __init__(self, lamp:Lamp, camera:Camera, stage:Stage, start=1350, images=40, step=1):
        super().__init__()
        self.images = images
        self.start = start
        self.step = step
        self.lamp = lamp
        self.camera = camera
        self.stage = stage

        self.lamp.set_on()
        # self.core.set_exposure(15)
        self.camera.set_option("Binning", "1x1")
        self.camera.set_option("PixelType", "GREY8")
        self.camera.set_option("ExposureAuto", "0")

    
    def focus(self):
        offset = self.images // 2

        for z_val in range(self.start - offset, self.start + offset + 2, self.step):
            img = self.camera.snap_image()

            if self.camera.byte_depth == 1:
                ip = np.reshape(img, (self.camera.height, self.camra.width)).astype(np.uint8)
            elif self.camera.byte_depth == 2:
                ip = np.reshape(img, (self.camera.height, self.camra.width)).astype(np.uint16)
            elif self.camera.byte_depth == 4:
                ip = np.reshape(img, (self.camera.height, self.camra.width)).astype(np.uint32)
            else:
                raise ValueError(f'byte depth should be 1, 2 or 4. byte depth: {self.camera.byte_depth}')
        
            img_index = z_val - self.start + offset

            if img_index == 0 or img_index == 1:
                pre_path = f"Autofocus/image_{img_index}.tif"
            else:
                pre_path = f"Autofocus/image_{img_index-2}.tif"
            
            tiff.imwrite(pre_path, ip) # photometric='minisblack'
            z_pos = z_val
            self.stage.move(z=z_pos)

        max_var, max_var_index, variances = -1, -1, []
        for i in range(self.images):
            image = tiff.imread(f"Autofocus/image_{i}.tif")
            mean, std = np.mean(image), np.std(image)
            norm_var = std * std / mean
            variances.append(norm_var)
            if norm_var > max_var:
                max_var, max_var_index = norm_var, i
        
        z_pos = (self.start - offset) + (self.step * max_var_index)
        self.stage.move(z=z_pos)
        return max_var_index, max_var, variances




class InPhase(Autofocus):
    def focus(self):
        pass

class LaserAutofocus(Autofocus):
    def focus(self):
        pass