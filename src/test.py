# from core.controller import controller
# from core.microscope import microscope
from core.autofocus import Autofocus, Amplitude, Phase, Laser

import tifffile as tiff
import matplotlib.pyplot as plt
import numpy as np

pre_path = "Autofocus/images/capture_33.tif"  
img = tiff.imread(pre_path)


plt.imshow(img, cmap='gray')  
plt.show()


img1 = np.max(img) - img
plt.imshow(img1, cmap='gray')  
plt.show()

import cv2
import numpy as np
import tifffile as tiff
import os

def detect_spot_and_measure(image):
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

image_dir = "Autofocus/images/"

# List all .tif files in the directory
image_files = [f for f in os.listdir(image_dir) if f.endswith('.tif')]
image_files.sort()  # Sort to ensure the files are in order

focus_scores = []

# Loop through each image file
for filename in image_files:
    img_path = os.path.join(image_dir, filename)
    img = tiff.imread(img_path)
    spot_area, spot_intensity = detect_spot_and_measure(img)
    
    # Calculate a focus score: higher intensity and smaller area is better
    focus_score = spot_intensity / (spot_area + 1e-10)  # Adding a small constant to avoid division by zero
    focus_scores.append(focus_score)

# Find the index of the image with the highest focus score
best_focus_index = np.argmax(focus_scores)
best_focus_image_path = os.path.join(image_dir, image_files[best_focus_index])

print(f"The best focused image is: {best_focus_image_path}")
