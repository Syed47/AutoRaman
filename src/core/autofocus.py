import cv2
import numpy as np
import tifffile as tiff
import os
import pandas as pd
from abc import ABC, abstractmethod

from core.camera import Camera, CCDCamera, SpectralCamera
from core.lamp import Lamp
from core.stage import Stage

from time import sleep

class Autofocus(ABC):
    def __init__(self, camera: Camera, stage: Stage, lamp: Lamp, image_dir=""):
        self.camera = camera
        self.lamp = lamp
        self.stage = stage
        self.image_dir = f"Autofocus/{image_dir}"
        self.focus_distance = None
        self.focused_image = None
        self.captures = []
        self.capture_scores = []
        os.makedirs(f"Autofocus/plots", exist_ok=True)
        os.makedirs(self.image_dir, exist_ok=True)

    def get_file_path(self, index: int) -> str:
        if isinstance(self.camera, CCDCamera):
            return f"{self.image_dir}/capture_{index}.tif"
        elif isinstance(self.camera, SpectralCamera):
            return f"{self.image_dir}/capture_{index}.csv"
        raise ValueError("Unsupported camera in class Autofocus")

    def zscan(self, start: int, end: int, step: int = 1, callback=lambda x: None) -> None:
        self.start = int(start)
        self.end = int(end)
        self.step = int(step)

        self.stage.move(z=self.start)
        sleep(2)

        for i, z_val in enumerate(range(self.start - self.step * 5, self.end + self.step, self.step)):
            try:
                img = self.camera.capture()
                self.stage.move(z=z_val + 5)
                sleep(1)

                if i < 5:
                    continue

                pre_path = self.get_file_path(i - 5)
                
                if isinstance(self.camera, CCDCamera):
                    tiff.imwrite(pre_path, img)
                elif isinstance(self.camera, SpectralCamera):
                    pd.DataFrame(img).to_csv(pre_path) 

                self.captures.append(pre_path)
                callback(pre_path)

            except Exception as e:
                print(f"Error capturing at z={z_val}: {e}")

        # self.stage.move(z=self.start)

    @abstractmethod
    def focus(self, start: int, end: int, step: int, callback=None) -> float:
        pass

# Placeholder class for manually setting autofocus using a precaptured image
class Manual(Autofocus):
    def __init__(self, camera, stage, lamp, image_dir=""):
        super().__init__(camera, stage, lamp, image_dir)

    def focus(self, start: int, end: int, step: int, callback=None) -> float:
        image, distance =  callback()
        print(image, distance)
        self.focused_image = image
        self.focus_distance = distance
        return self.focus_distance

class Amplitude(Autofocus):
    def __init__(self, camera: Camera, stage: Stage, lamp: Lamp, image_dir="images"):
        super().__init__(camera, stage, lamp, image_dir)


    def focus(self, start: int, end: int, step: int, callback=None) -> float:
        self.zscan(start, end, step, callback)
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
        self.focused_image = self.get_file_path(max_index)
        print(self.focused_image)
        self.capture_scores = variances

        return self.focus_distance


class Phase(Autofocus):
    def __init__(self, camera: Camera, stage: Stage, lamp: Lamp, image_dir="images"):
        super().__init__(camera, stage, lamp, image_dir)

    def focus(self, start: int, end: int, step: int, callback=None) -> float:
        self.zscan(start, end, step, callback)
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

        self.focus_distance = self.start + self.step * min_index
        self.focused_image = self.get_file_path(min_index)
        print(self.focused_image)
        self.capture_scores = variances

        return self.focus_distance

class Laser(Autofocus):
    def __init__(self, camera: Camera, stage: Stage, lamp: Lamp, image_dir="laser"):
        super().__init__(camera, stage, lamp, image_dir)

    def focus(self, start: int, end: int, step: int, callback=None) -> float:
        self.zscan(start, end, step, callback)
        # self.captures.sort()
        focus_scores = []

        for imagefile in self.captures:
            img = tiff.imread(imagefile)
            spot_area, spot_intensity = self.detect_spot_and_measure(img)
            focus_score = spot_intensity / (spot_area + 1e-10)
            focus_scores.append(focus_score)
        
        focus_scores = np.array(focus_scores)

        min_score = np.min(focus_scores)
        max_score = np.max(focus_scores)
        
        if max_score > min_score:
            normalized_scores = (focus_scores - min_score) / (max_score - min_score)
        else:
            normalized_scores = np.zeros_like(focus_scores)

        best_focus_index = np.argmax(normalized_scores)
        best_focus_image_path = self.captures[best_focus_index]

        print(f"The best focused image is: {best_focus_image_path}")
        self.focus_distance = self.start + self.step * best_focus_index
        self.focused_image = best_focus_image_path
        print(self.focused_image)
        self.capture_scores = normalized_scores
        print(self.focus_distance)
        return self.focus_distance

    def detect_spot_and_measure(self, image):
        gray = np.max(image) - image
        blurred = cv2.GaussianBlur(gray, (5, 5), 0)
        _, thresh = cv2.threshold(blurred, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
        contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        if contours:
            max_contour = max(contours, key=cv2.contourArea)
            spot_area = cv2.contourArea(max_contour)
            spot_intensity = cv2.mean(gray, mask=cv2.drawContours(np.zeros_like(gray), [max_contour], -1, 255, thickness=-1))[0]
        else:
            spot_area = float('inf') 
            spot_intensity = 0

        return spot_area, spot_intensity


from scipy.signal import find_peaks


class RamanSpectra(Autofocus):
    def __init__(self, camera: Camera, stage: Stage, lamp: Lamp, image_dir="spectra"):
        super().__init__(camera, stage, lamp, image_dir)

    def focus(self, start: int, end: int, step: int, callback=None) -> float:
        pass
    
    @staticmethod
    def find_best_spectrum(wavelengths, spectra, min_wavelength=500, max_wavelength=700):
        best_spectrum = None
        highest_peak_sum = 0
        best_spectrum_index = -1

        for i, intensities in enumerate(spectra):
            mask = (wavelengths >= min_wavelength) & (wavelengths <= max_wavelength)
            focused_wavelengths = wavelengths[mask]
            focused_intensities = intensities[mask]
            
            peak_indices, _ = find_peaks(focused_intensities)
            peak_intensities = focused_intensities[peak_indices]
            
            if len(peak_intensities) < 2:
                continue
            
            sorted_peak_intensities = np.sort(peak_intensities)[-2:]
            peak_sum = np.sum(sorted_peak_intensities)
            
            if peak_sum > highest_peak_sum:
                highest_peak_sum = peak_sum
                best_spectrum = intensities
                best_spectrum_index = i

        return best_spectrum, best_spectrum_index