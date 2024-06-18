
import matplotlib.pyplot as plt
import tifffile as tiff
import numpy as np
import skimage as ski
import os
import time
from abc import ABC, abstractmethod

from os.path import join
from pycromanager import Core, start_headless, stop_headless


class Lamp:
    def __init__(self, core:Core=None):
        self.core = core
    
    def set_on(self):
        self.core.set_property("TransmittedLamp", "Label", "On")
    
    def set_off(self):
        self.core.set_property("TransmittedLamp", "Label", "Off")

class Camera:
    def __init__(self, core:Core=None, camera:str='AmScope', exposure:int=15):
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
    
class Stage:
    def __init__(self, core:Core=None):
        self.core = core
        self.vertical = self.core.get_focus_device()
        self.horizontal = self.core.get_xy_stage_device()
        self.x = self.core.get_x_position(self.horizontal)
        self.x = self.core.get_y_position(self.horizontal)
        self.z = self.core.get_position(self.vertical)
    
    def move(self, x=0, y=0, z=0):
        self.x += x
        self.y += y
        self.z += z


class Autofocus(ABC):
    def __init__(self, core:Core=None):
        self.core = core

    @abstractmethod
    def focus(self):
        pass

class Raman(Autofocus):
    def __init__(self, core:Core=None, z_start=1350, images=40):
        super().__init__(core)
        self.images = images

    def focus(self):
        offset = self.images // 2

        for z_val in range(z_start - offset, z_start + offset + 2, step):

            img_index = z_val - z_start + offset

            if img_index == 0 or img_index == 1:
                pre_path = join(path, f"Autofocus/image_{img_index}.tif")
            else:
                pre_path = join(path, f"Autofocus/image_{img_index-2}.tif")
            
            tiff.imwrite(pre_path, ip) # photometric='minisblack'
            z_pos = z_val
            self.core.set_position(zstage, z_pos)

        max_var, max_var_index, variances = -1, -1, []
        for i in range(self.images):
            image = tiff.imread(join(path, f"Autofocus/image_{i}.tif"))
            mean, std = np.mean(image), np.std(image)
            norm_var = std * std / mean
            variances.append(norm_var)
            if norm_var > max_var:
                max_var, max_var_index = norm_var, i
        
        z_pos = (z_start - offset) + (step * max_var_index)
        self.core.set_position(zstage, z_pos)
        return max_var_index, max_var, variances

class InPhase(Autofocus):
    def focus(self):
        pass


class Microscope:
    def __init__(self, headless=True, config_file:str=None):
        self.core_app_path = "C:\\Program Files\\Micro-Manager-2.0"
        self.config_file = f"{self.core_app_path}\\IX81_LUDL_amscope_Laser532.cfg"
        if headless:
            start_headless(self.core_app_path, config_file, debug=False)
        self.core = Core()            
        self.core.load_system_configuration(config_file)
