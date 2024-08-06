# import cellpose as cp

# print(dir(cp))
# # from cellpose.io import imread

# import os


# files = []
# for root, dirs, filenames in os.walk('..\\Autofocus'):
#     for filename in filenames:
#         files.append(os.path.join(root, filename))

# print(files)


# # model_type='cyto' or model_type='nuclei'
# model = models.Cellpose(gpu=False, model_type='cyto')

# files = ['img0.tif', 'images/capture.tif']
# imgs = [imread(f) for f in files]
# masks, flows, styles, diams = model.eval(imgs, diameter=None, channels=[0,0


# # Test Script
from core.controller import controller
from core.microscope import microscope
from core.autofocus import Amplitude, Phase
import os
# from time import sleep
# # creating required directories
# os.makedirs('Autofocus/images', exist_ok=True)
os.makedirs('images', exist_ok=True)
# os.makedirs('Stitches', exist_ok=True)
# os.makedirs('Results', exist_ok=True)

# controller.config_file = "IX81_LUDL_amscope_Laser532.cfg"

# ms = Microscope()

microscope.camera.set_option("Binning", "1x1")
microscope.camera.set_option("PixelType", "GREY8")
microscope.camera.set_option("ExposureAuto", "0")
microscope.camera.set_exposure(15)

# result = microscope.auto_focus(strategy=Amplitude, start=1310, end=1350)
# print(result)



import matplotlib.pyplot as plt
import numpy as np
import tifffile as tiff

for i in range(0, 10):
    img = microscope.snap_image(i/10)
    pre_path = f"images/capture_{1+i}.tif"
    tiff.imwrite(pre_path, img)

