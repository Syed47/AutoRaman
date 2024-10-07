from abc import ABC, abstractmethod
from skimage.feature import peak_local_max
import numpy as np
import tifffile as tiff
from cellpose import models
from cellpose.io import imread
from scipy.ndimage import center_of_mass

class ICellIdentifier(ABC):
    def __init__(self):
        pass

    @abstractmethod
    def identify(self, image: np.ndarray, min_distance: int, threshold_abs: int) -> np.ndarray:
        pass

class CustomCellIdentifier(ICellIdentifier):
    def __init__(self):
        super().__init__()

    def identify(self, image: np.ndarray, min_distance: int = 60, threshold_abs: int = 5) -> np.ndarray:
        cells = peak_local_max(image, min_distance=min_distance, threshold_abs=threshold_abs)
        return cells.tolist()

# based on the CellPose algorithm
class CellPose(ICellIdentifier):
    def __init__(self):
        super().__init__()

    def identify_cells(self, image: np.ndarray, diameter: int = 100, threshold: int = 0.8):
        cyto_model = models.Cellpose(gpu=False, model_type='cyto')
        cyto_mask, cyto_flows, cyto_styles, cyto_diams = cyto_model.eval(
            image, diameter=diameter, channels=[0, 0], flow_threshold=threshold, do_3D=False)

        return cyto_mask

    def identify_nuclei(self, image: np.ndarray, diameter: int = 100, threshold: int = 0.8):
        nuclei_model = models.Cellpose(gpu=False, model_type='nuclei')
        nuclei_mask, nuclei_flows, nuclei_styles, nuclei_diams = nuclei_model.eval(
            image, diameter=diameter, channels=[0, 0], flow_threshold=threshold, do_3D=False)
        
        unique_nuclei = np.unique(nuclei_mask)
        centroids = []
        for nucleus in unique_nuclei:
            if nucleus == 0:
                continue
            nucleus_mask = nuclei_mask == nucleus
            centroid = center_of_mass(nucleus_mask)
            centroids.append(centroid)

        return nuclei_mask, centroids

    def identify(self, image: np.ndarray, diameter: int = 100, threshold: int = 0.8, model: list = ['cyto', 'nuclei']):
        cyto_result = None
        nuclei_result = None

        if 'cyto' in model:
            cyto_result = self.identify_cells(image, diameter, threshold)
        
        if 'nuclei' in model:
            nuclei_result = self.identify_nuclei(image, diameter, threshold)

        return cyto_result, nuclei_result