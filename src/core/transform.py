from core.microscope import microscope

import numpy as np
import tifffile as tiff
import time
import cv2

class Transform:

    def __init__(self):
        self._matrix = None

      
    def matrix(self) -> np.ndarray:
        pass


img1 = "Autofocus/transform/image-1.tif"
img2 = "Autofocus/transform/image-2.tif"

img = microscope.snap_image()
img = microscope.snap_image()
img = microscope.snap_image()
img = microscope.snap_image()
img = microscope.snap_image()
img = microscope.snap_image()
img = microscope.snap_image()

img = microscope.snap_image()
tiff.imwrite(img1, img)

x = microscope.stage.x
y = microscope.stage.y

microscope.move_stage(self.stage_to_camera_width, self.stage_to_camera_height, 0)
time.sleep(2)
img = microscope.snap_image()
img = microscope.snap_image()
img = microscope.snap_image()
img = microscope.snap_image()
img = microscope.snap_image()
img = microscope.snap_image()
tiff.imwrite(img2, img)

print("camera width:", microscope.camera.width)

self.image1 = QPixmap(img1)
self.img1.setPixmap(self.image1)

self.image2 = QPixmap(img2)
self.img2.setPixmap(self.image2)

stage_shift_x = microscope.stage.x - x

image1 = cv2.imread(img1, cv2.IMREAD_GRAYSCALE) 
image2 = cv2.imread(img2, cv2.IMREAD_GRAYSCALE)

image1 = cv2.normalize(image1, None, alpha=0, beta=255, norm_type=cv2.NORM_MINMAX)
image2 = cv2.normalize(image2, None, alpha=0, beta=255, norm_type=cv2.NORM_MINMAX)

half_width = image1.shape[1] // 2
# half_height = image1.shape[0] // 2
left_half_image1 = image1[:, :half_width]
right_half_image2 = image2[:, half_width:]

shift_result = cv2.phaseCorrelate(np.float32(left_half_image1), np.float32(right_half_image2))
detected_shift = shift_result[0]

actual_shift_x = detected_shift[0] + half_width
actual_shift_y = detected_shift[1]

print(f"Exact shift in pixels: X: {actual_shift_x}, Y: {actual_shift_y}")

blended_image = np.zeros((left_half_image1.shape[0], left_half_image1.shape[1], 3), dtype=np.uint8)
blended_image[..., 0] = left_half_image1  # Red channel
blended_image[..., 1] = cv2.warpAffine(right_half_image2, np.float32([[1, 0, -detected_shift[0]], [0, 1, -detected_shift[1]]]), (right_half_image2.shape[1], right_half_image2.shape[0]))  # Green channel

plt.figure(figsize=(8, 16))
plt.imshow(blended_image)
plt.axis('off')
plt.subplots_adjust(left=0, right=1, top=1, bottom=0)
plt.savefig("Autofocus/transform/overlap.png", bbox_inches='tight', pad_inches=0)
plt.close()
self.overlap_image = QPixmap("Autofocus/transform/overlap.png")
self.img_overlap.setPixmap(self.overlap_image)

a = actual_shift_x / stage_shift_x
c = actual_shift_y / stage_shift_x

theta = np.arctan2(c, a)
M = a / np.cos(theta) 

b = -M * np.sin(theta)
d = M * np.cos(theta)

print(f"Rotation (theta): {np.degrees(theta)} degrees")
print(f"Scaling (M): {M}")
print(f"Transformation matrix: [[{a:.2f}, {b:.2f}], [{c:.2f}, {d:.2f}]]")

def predict_stage_movement(px, py):
    T_inv = np.linalg.inv(np.array([[a, b], [c, d]]))
    return T_inv.dot(np.array([px, py]))

px_shift, py_shift = int(self.txt_pixel_shift_x.text()), int(self.txt_pixel_shift_y.text()) 
print(f"Pixel X shift: {px_shift}, Pixel Y shift: {py_shift}")
stage_movement = predict_stage_movement(px_shift, py_shift)
print(f"Stage X movement: {stage_movement[0]:.2f} um, Stage Y movement: {stage_movement[1]:.2f} um")

self.txt_stage_x.setText(f"{stage_movement[0]:.2f}")
self.txt_stage_y.setText(f"{stage_movement[1]:.2f}")
