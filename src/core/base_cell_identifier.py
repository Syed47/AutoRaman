from abc import ABC, abstractmethod
from skimage.feature import peak_local_max
import numpy as np

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

    def identify(self, image: np.ndarray, min_distance: int = 60, threshold_abs: int = 5) -> np.ndarray:
        pass