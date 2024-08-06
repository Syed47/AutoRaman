import tifffile as tiff
import numpy as np
import pandas as pd
from abc import ABC, abstractmethod

from core.camera import ICamera, Camera, SpectralCamera
from core.lamp import Lamp
from core.stage import Stage

from time import sleep
from os import makedirs

class Autofocus(ABC):
    def __init__(self, camera: ICamera, stage: Stage, lamp: Lamp, image_dir="Autofocus"):
        self.camera = camera
        self.lamp = lamp
        self.stage = stage
        self.image_dir = image_dir
        self.focus_distance = None
        self.focused_image = None
        self.captures = []
        self.batch_variance = []
        makedirs(f"{self.image_dir}/images", exist_ok=True)
        makedirs(f"{self.image_dir}/spectra", exist_ok=True)
        makedirs(f"{self.image_dir}/plots", exist_ok=True)


    def zscan(self, start: int, end: int, step: int = 1) -> None:
        self.start = int(start)
        self.end = int(end)
        self.step = int(step)
        self.stage.move(z=self.start)
        self.lamp.set_on()
        sleep(1)

        for i, z_val in enumerate(range(self.start-3, self.end, self.step)):
            try:
                img = self.camera.capture()
                if i <= 2: continue # discarding first 3 images for important reason !!!!
                if isinstance(self.camera, Camera):
                    pre_path = f"{self.image_dir}/images/capture_{i-2}.tif"
                    tiff.imwrite(pre_path, img)
                    self.captures.append(pre_path)
                elif isinstance(self.camera, SpectralCamera):
                    pre_path = f"{self.image_dir}/spectra/capture_{i-2}.csv"
                    pd.write_csv(pre_path, img)
                    self.captures.append(pre_path)
            except Exception as e:
                print(f"Error capturing at z={z_val}: {e}")
            self.stage.move(z=z_val)
            sleep(0.5)

        self.stage.move(z=start)
        self.lamp.set_off()

    @abstractmethod
    def focus(self, start: int, end: int, step: int) -> float:
        pass


class Amplitude(Autofocus):
    def __init__(self, camera: ICamera, stage: Stage, lamp: Lamp, image_dir="Autofocus"):
        super().__init__(camera, stage, lamp, image_dir)


    def focus(self, start: int, end: int, step: int) -> float:
        self.zscan(start, end, step)
        print("zscan done")
        max_var, max_index, variances = -1, -1, []

        for i, capture_path in enumerate(self.captures):
            try:
                image = tiff.imread(capture_path)
                mean = np.mean(image)
                if mean == 0:
                    continue
                std = np.std(image)
                norm_var = std * std / mean
                variances.append(norm_var)
                if norm_var > max_var:
                    max_var, max_index = norm_var, i
            except Exception as e:
                print(f"Error processing capture {i}: {e}")

        self.focus_distance = self.start + self.step * max_index
        self.focused_image = f"{self.image_dir}/images/capture_{max_index+1}.tif"
        print(self.focused_image)
        self.batch_variance = variances
        return self.focus_distance


class Phase(Autofocus):
    def __init__(self, camera: ICamera, stage: Stage, lamp: Lamp, image_dir="Autofocus"):
        super().__init__(camera, stage, lamp, image_dir)

    def focus(self, start: int, end: int, step: int) -> float:
        self.zscan(start, end, step)
        min_var, min_index, variances = 1e10, -1, []

        for i, capture_path in enumerate(self.captures):
            try:
                image = tiff.imread(capture_path)
                mean = np.mean(image)
                if mean == 0:
                    continue
                std = np.std(image)
                norm_var = std * std / mean
                variances.append(norm_var)
                if norm_var < min_var:
                    min_var, min_index = norm_var, i
            except Exception as e:
                print(f"Error processing capture {i}: {e}")

        return self.start + self.step * min_index


class Laser(Autofocus):
    def focus(self, start: int, end: int, step: int) -> float:
        pass


class RamanSpectra(Autofocus):
    def focus(self, start: int, end: int, step: int) -> float:
        pass
