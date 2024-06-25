import tifffile as tiff
import numpy as np
from abc import ABC, abstractmethod
from enum import Enum
from pycromanager import Core

from Lamp import Lamp
from Stage import Stage
from Camera import Camera

class Autofocus(ABC):

    def __init__(self, camera, lamp, stage, image_dir="Autofocus"):
        self.camera = camera
        self.lamp = lamp
        self.stage = stage
        self.image_dir = image_dir

    def zscan(self, start=1350, end=1400, step=1) -> None:
        self.lamp.set_on()
        self.images = (end - start) // step

        for i, z_val in enumerate(range(start, end, step)):
            pre_path = f"{self.image_dir}/image_{i}.tif"
            try:
                img = self.camera.snap_image()
                tiff.imwrite(pre_path, img)
            except Exception as e:
                print(f"Error capturing image at z={z_val}: {e}")
            self.stage.move(z=z_val)

        self.stage.move(z=start)
        self.lamp.set_off()

    @abstractmethod
    def focus(self):
        pass


class BrightSpot(Autofocus):

    def __init__(self, camera=None, lamp=None, stage=None, image_dir="Autofocus"):
        super().__init__(camera, lamp, stage, image_dir)

    def focus(self) -> tuple:
        max_var, max_index, variances = -1, -1, []

        for i in range(self.images):
            try:
                image = tiff.imread(f"{self.image_dir}/image_{i}.tif")
                mean = np.mean(image)
                if mean == 0: continue
                std = np.std(image)
                norm_var = std * std / mean
                variances.append(norm_var)
                if norm_var > max_var:
                    max_var, max_index = norm_var, i
            except Exception as e:
                print(f"Error processing image {i}: {e}")

        return max_index, max_var, variances


class InPhase(Autofocus):
    def focus(self):
        pass


class Laser(Autofocus):
    def focus(self):
        pass

