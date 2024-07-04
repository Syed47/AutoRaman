# Test Script
from controller import controller
from microscope import Microscope
from autofocus import Amplitude, Phase, RamanSpectra
import os
from time import sleep
# creating required directories
os.makedirs('Autofocus/images', exist_ok=True)
os.makedirs('images', exist_ok=True)
os.makedirs('Stitches', exist_ok=True)
os.makedirs('Results', exist_ok=True)

controller.config_file = "IX81_LUDL_amscope_Laser532.cfg"

ms = Microscope()

# ms.camera.set_option("Binning", "1x1")
# ms.camera.set_option("PixelType", "GREY8")
# ms.camera.set_option("ExposureAuto", "0")
ms.camera.set_exposure(15)

# result = ms.auto_focus(strategy=Amplitude, start=1310, end=1350)
# print(result)



import matplotlib.pyplot as plt
import numpy as np
import tifffile as tiff

for i in range(0, 10):
    img = ms.snap_image(i/10)
    pre_path = f"images/capture_{1+i}.tif"
    tiff.imwrite(pre_path, img)

