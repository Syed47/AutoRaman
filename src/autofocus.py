import tifffile as tiff
import numpy as np
import pandas as pd
from abc import ABC, abstractmethod

from camera import ICamera, Camera, SpectralCamera
from lamp import Lamp
from stage import Stage

from time import sleep

class Autofocus(ABC):
    def __init__(self, camera: ICamera, stage: Stage, lamp: Lamp, image_dir="Autofocus"):
        self.camera = camera
        self.lamp = lamp
        self.stage = stage
        self.image_dir = image_dir
        self.captures = []

    def zscan(self, start: int, end: int, step: float = 1) -> None:
        self.start = start
        self.end = end
        self.step = step
        self.stage.move(z=self.start)
        self.lamp.set_on()
        sleep(1)

        for i, z_val in enumerate(range(start-3, end, step)):
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
    def focus(self, start: int, end: int, step: float) -> float:
        pass


class Amplitude(Autofocus):
    def __init__(self, camera: ICamera, stage: Stage, lamp: Lamp, image_dir="Autofocus"):
        super().__init__(camera, stage, lamp, image_dir)

    def focus(self, start: int, end: int, step: float) -> float:
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

        return self.start + self.step * max_index


class Phase(Autofocus):
    def __init__(self, camera: ICamera, stage: Stage, lamp: Lamp, image_dir="Autofocus"):
        super().__init__(camera, stage, lamp, image_dir)

    def focus(self, start: int, end: int, step: float) -> float:
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
    def focus(self, start: int, end: int, step: float) -> float:
        pass


class RamanSpectra(Autofocus):
    def focus(self, start: int, end: int, step: float) -> float:
        pass