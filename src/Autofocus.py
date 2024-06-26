import tifffile as tiff
import numpy as np
import pandas as pd
from abc import ABC, abstractmethod
from enum import Enum
from pycromanager import Core

from Microscope import Microscope

class Autofocus(ABC):

    def __init__(self, microscope:Microscope, image_dir="Autofocus"):
        self.camera = microscope.camera
        self.lamp = microscope.lamp
        self.stage = microscope.stage
        self.image_dir = image_dir
        self.captures = []

    def zscan(self, start=1350, end=1400, step=1) -> list:
        self.lamp.set_on()

        for i, z_val in enumerate(range(start, end, step)):
            try:
                img = self.camera.capture()
                if isinstance(self.camera, Camera): 
                    pre_path = f"{self.image_dir}/images/capture_{i}.tif"
                    tiff.imwrite(pre_path, img)
                    self.captures.append(pre_path)
                elif isinstance(self.camera, SpectralCamera):
                    pre_path = f"{self.image_dir}/spectra/capture_{i}.csv"
                    pd.write_csv(pre_path, img)
                    self.captures.append(pre_path)
            except Exception as e:
                print(f"Error capturing at z={z_val}: {e}")
            self.stage.move(z=z_val)

        self.stage.move(z=start)
        self.lamp.set_off()
        return self.captures

    @abstractmethod
    def focus(self) -> float:
        pass


class Amplitude(Autofocus):

    def __init__(self, microscope:Microscope, image_dir="Autofocus"):
        super().__init__(microscope, image_dir)

    def focus(self, start=1350, end=1400, step=1) -> float:
        self.zscan()
        max_var, max_index, variances = -1, -1, []

        for i in range(self.images):
            try:
                image = tiff.imread(f"{self.image_dir}/images/capture_{i}.tif")
                mean = np.mean(image)

                if mean == 0: continue
                std = np.std(image)
                norm_var = std * std / mean
                variances.append(norm_var)
                if norm_var > max_var:
                    max_var, max_index = norm_var, i
            except Exception as e:
                print(f"Error processing {i}: {e}")

        return start + step * max_index


class Phase(Autofocus):

    def __init__(self, microscope:Microscope, image_dir="Autofocus"):
        super().__init__(microscope, image_dir)

    def focus(self) -> float:
        min_var, min_index, variances = 1e10, -1, []

        for i in range(self.images):
            try:
                image = tiff.imread(f"{self.image_dir}/images/capture_{i}.tif")
                mean = np.mean(image)

                if mean == 0: continue
                std = np.std(image)
                norm_var = std * std / mean
                variances.append(norm_var)
                if norm_var < min_var:
                    min_var, min_index = norm_var, i
            except Exception as e:
                print(f"Error processing {i}: {e}")

        return return start + step * max_index


class Laser(Autofocus):
    def focus(self):
        pass
        # return start + step * max_index


class RamanSpectra(Autofocus):
    def focus(self):
        min_var, min_index, variances = 1e10, -1, []

        for i in range(self.images):
            try:
                image = tiff.imread(f"{self.image_dir}/spectra/capture_{i}.tif")
                # mean = np.mean(image)

                # if mean == 0: continue
                # std = np.std(image)
                # norm_var = std * std / mean
                # variances.append(norm_var)
                # if norm_var < min_var:
                #     min_var, min_index = norm_var, i
            except Exception as e:
                print(f"Error processing spectra {i}: {e}")

        return return start + step * max_index
