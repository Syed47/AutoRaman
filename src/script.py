import os
os.environ['KMP_DUPLICATE_LIB_OK'] = 'True'
import numpy as np
from cellpose import models
from cellpose.io import imread
import matplotlib.pyplot as plt
from scipy.ndimage import center_of_mass

cyto_model = models.Cellpose(gpu=False, model_type='cyto')
nuclei_model = models.Cellpose(gpu=False, model_type='nuclei')

img = imread("Autofocus/images/capture_1.tif")

cyto_masks, cyto_flows, cyto_styles, cyto_diams = cyto_model.eval(
    img, diameter=110, channels=[0, 0], flow_threshold=0.9, do_3D=False)

nuclei_masks, nuclei_flows, nuclei_styles, nuclei_diams = nuclei_model.eval(
    img, diameter=110, channels=[0, 0], flow_threshold=0.9, do_3D=False)

cyto_mask = cyto_masks
nuclei_mask = nuclei_masks

plt.imshow(img, cmap='gray')
plt.imshow(nuclei_mask, cmap='cool', alpha=0.5)
plt.imshow(cyto_mask, cmap='jet', alpha=0.5)

unique_nuclei = np.unique(nuclei_mask)

for nucleus in unique_nuclei:
    if nucleus == 0:
        continue
    nucleus_mask = nuclei_mask == nucleus
    centroid = center_of_mass(nucleus_mask)
    plt.plot(centroid[1], centroid[0], 'ro', markersize=2)

plt.title('Segmentation with Nuclei Centers')
plt.axis('off')
plt.show()
plt.close()
