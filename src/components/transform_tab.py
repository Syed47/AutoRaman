from PyQt5.QtWidgets import QFileDialog, QWidget, QHBoxLayout, QGridLayout, QVBoxLayout, QFrame, QSlider, QCheckBox, QComboBox, QLabel, QLineEdit, QPushButton
from PyQt5.QtGui import QPixmap, QImage
from PyQt5.QtCore import Qt, QTimer

from components.tab import Tab
from core.microscope import microscope
from core.controller import controller
from components.state import state_manager

import cv2
import numpy as np
import matplotlib.pyplot as plt
import tifffile as tiff
import os
import time

class TransformTab(Tab):

    def __init__(self, logger=None):
        super().__init__(logger)
        self.init_ui()
        self.connect_signals()
        os.makedirs(f"Autofocus/transform", exist_ok=True)

    def preprocess(self):
        pass

    def postprocess(self):
        pass

    def connect_signals(self):
        pass

    def init_ui(self):
        tab_layout = QHBoxLayout()
        
        frame_tab = QFrame()
        frame_tab.setFrameShape(QFrame.StyledPanel)
        frame_tab_layout = QHBoxLayout()
        
        left_panel = QFrame()
        left_panel.setStyleSheet("QFrame { border: 1px solid #444444; };")  
        left_panel.setFixedSize(320, 540)
        
        self.checkbox_shift = QCheckBox("Edit Shift", left_panel)
        self.checkbox_shift.setGeometry(140, 10, 160, 40)
        self.checkbox_shift.setChecked(False)

        radio_label = QLabel("Shift X:", left_panel)
        radio_label.setGeometry(40, 60, 140, 40)
        radio_label.setStyleSheet("QLabel { border: none; font-size:16px; };")
        self.txt_shift_x = QLineEdit(left_panel)
        self.txt_shift_x.setPlaceholderText("10 (μm)")
        self.txt_shift_x.setStyleSheet("QLineEdit { font-size:16px; };")
        self.txt_shift_x.setGeometry(160, 60, 100, 40)
        self.txt_shift_x.setReadOnly(True)

        line_label1 = QLabel("Shift Y:", left_panel)
        line_label1.setGeometry(40, 120, 100, 40)
        line_label1.setStyleSheet("QLabel { border: none; font-size:16px; };")
        self.txt_shift_y = QLineEdit(left_panel)
        self.txt_shift_y.setPlaceholderText("1350 (μm)")
        self.txt_shift_y.setStyleSheet("QLineEdit { font-size:16px; };")
        self.txt_shift_y.setGeometry(160, 120, 100, 40)
        self.txt_shift_y.setReadOnly(True)

        line_separator2 = QFrame(left_panel)
        line_separator2.setGeometry(0, 180, 400, 1)
        line_separator2.setFrameShape(QFrame.HLine)
        line_separator2.setFrameShadow(QFrame.Sunken)

        line_label2 = QLabel("Pixel Shift X:", left_panel)
        line_label2.setGeometry(40, 200, 100, 40)
        line_label2.setStyleSheet("QLabel { border: none; font-size:16px; };")
        self.txt_pixel_shift_x = QLineEdit(left_panel)
        self.txt_pixel_shift_x.setPlaceholderText("1400 (μm)")
        self.txt_pixel_shift_x.setStyleSheet("QLineEdit { font-size:16px; };")
        self.txt_pixel_shift_x.setGeometry(160, 200, 100, 40)

        line_label3 = QLabel("Pixel Shift Y:", left_panel)
        line_label3.setGeometry(40, 260, 100, 40)
        line_label3.setStyleSheet("QLabel { border: none; font-size:16px; };")
        self.txt_pixel_shift_y = QLineEdit(left_panel)
        self.txt_pixel_shift_y.setPlaceholderText("1 (μm)")
        self.txt_pixel_shift_y.setStyleSheet("QLineEdit { font-size:16px; };")
        self.txt_pixel_shift_y.setGeometry(160, 260, 100, 40)
        
        line_separator2 = QFrame(left_panel)
        line_separator2.setGeometry(0, 320, 400, 1)
        line_separator2.setFrameShape(QFrame.HLine)
        line_separator2.setFrameShadow(QFrame.Sunken)

        self.btn_run = QPushButton("Transform", left_panel)
        self.btn_run.setGeometry(80, 340, 160, 40)
        
        line_separator2 = QFrame(left_panel)
        line_separator2.setGeometry(0, 400, 400, 1)
        line_separator2.setFrameShape(QFrame.HLine)
        line_separator2.setFrameShadow(QFrame.Sunken)

        line_x = QLabel("Stage Movement X:", left_panel)
        line_x.setGeometry(20, 420, 140, 40)
        line_x.setStyleSheet("QLabel { border: none; font-size:16px; };")
        self.txt_stage_x = QLineEdit(left_panel)
        self.txt_stage_x.setPlaceholderText("320 (μm)")
        self.txt_stage_x.setStyleSheet("QLineEdit { font-size:16px; };")
        self.txt_stage_x.setGeometry(180, 420, 100, 40)
        self.txt_stage_x.setReadOnly(True)

        line_label_y = QLabel("Stage Movement Y:", left_panel)
        line_label_y.setGeometry(20, 480, 140, 40)
        line_label_y.setStyleSheet("QLabel { border: none; font-size:16px; };")
        self.txt_stage_y = QLineEdit(left_panel)
        self.txt_stage_y.setPlaceholderText("450 (μm)")
        self.txt_stage_y.setStyleSheet("QLineEdit { font-size:16px; };")
        self.txt_stage_y.setGeometry(180, 480, 100, 40)
        self.txt_stage_y.setReadOnly(True)

        right_panel = QFrame()
        right_panel.setStyleSheet("QFrame { border: 1px solid #444444; };")  
        right_panel.setFixedSize(420, 540)

        self.image1 = QPixmap("components/microscope.png")
        self.img1 = QLabel(right_panel)
        self.img1.setStyleSheet("QLabel { border: 1px solid #444444; border-radius: 0px; };")
        self.img1.setPixmap(self.image1)
        self.img1.setFixedSize(200, 260)
        self.img1.setGeometry(10, 5, 200, 260)
        self.img1.setScaledContents(True)

        self.image2 = QPixmap("components/microscope.png")
        self.img2 = QLabel(right_panel)
        self.img2.setStyleSheet("QLabel { border: 1px solid #444444; border-radius: 0px; };")
        self.img2.setPixmap(self.image2)
        self.img2.setFixedSize(200, 260)
        self.img2.setGeometry(210, 5, 200, 260)
        self.img2.setScaledContents(True)

        self.overlap_image = QPixmap("components/microscope.png")
        self.img_overlap = QLabel(right_panel)
        self.img_overlap.setStyleSheet("QLabel { border: 1px solid #444444; border-radius: 0px; };")
        self.img_overlap.setPixmap(self.overlap_image)
        self.img_overlap.setFixedSize(200, 260)
        self.img_overlap.setGeometry(120, 275, 200, 260)
        self.img_overlap.setScaledContents(True)

        frame_tab_layout.addWidget(left_panel)
        frame_tab_layout.addWidget(right_panel)
        frame_tab.setLayout(frame_tab_layout)

        tab_layout.addWidget(frame_tab)
        self.setLayout(tab_layout)

    def connect_signals(self):
        # self.btn_run.clicked.connect(self.transform)
        self.checkbox_shift.clicked.connect(self.handle_manual_shift)

    def handle_manual_shift(self):
        checked = self.checkbox_shift.isChecked()
        self.txt_shift_x.setReadOnly(not checked)
        self.txt_shift_y.setReadOnly(not checked)
    
    def update(self):
        pass

    def transform(self):
        
        img1 = "Autofocus/transform/image-1.tif"
        img2 = "Autofocus/transform/image-2.tif"

        img = microscope.snap_image()
        tiff.imwrite(img1, img)
        
        x = microscope.stage.x
        y = microscope.stage.y

        img = microscope.snap_image()
        tiff.imwrite(img2, img)

        self.image1 = QPixmap(img1)
        self.img1.setPixmap(self.plot_bf)

        self.image2 = QPixmap(img2)
        self.img2.setPixmap(self.plot_bf)

        stage_shift_x = microscope.stage.x - x
        stage_shift_Y = microscope.stage.y - y

        # Load your images
        image1 = cv2.imread(img1, cv2.IMREAD_GRAYSCALE)  # Reference image
        image2 = cv2.imread(img2, cv2.IMREAD_GRAYSCALE)  # Translated image
        
        # Normalize images to [0, 255] range
        image1 = cv2.normalize(image1, None, alpha=0, beta=255, norm_type=cv2.NORM_MINMAX)
        image2 = cv2.normalize(image2, None, alpha=0, beta=255, norm_type=cv2.NORM_MINMAX)
        
        # Extract the left half of image1 and the right half of image2
        half_width = image1.shape[1] // 2
        left_half_image1 = image1[:, :half_width]
        right_half_image2 = image2[:, half_width:]
        
        # Calculate shift using phase correlation
        shift_result = cv2.phaseCorrelate(np.float32(left_half_image1), np.float32(right_half_image2))
        detected_shift = shift_result[0]
        
        # Account for the initial preprocessing displacement
        # Assuming right half of image2 starts half an image width offset from the start of image1
        actual_shift_x = detected_shift[0] + half_width
        actual_shift_y = detected_shift[1]
        
        # Print out the exact shift in pixels
        print(f"Exact shift in pixels: X: {actual_shift_x}, Y: {actual_shift_y}")
        
        
        #############################################################################################################################
        ## TEST the following code can be blanked out - it just helps us visualise if we have the correct shifts calculed
        # Optional: Visual confirmation
        # Create a blank RGB image for visualization
        blended_image = np.zeros((left_half_image1.shape[0], left_half_image1.shape[1], 3), dtype=np.uint8)
        blended_image[..., 0] = left_half_image1  # Red channel
        blended_image[..., 1] = cv2.warpAffine(right_half_image2, np.float32([[1, 0, -detected_shift[0]], [0, 1, -detected_shift[1]]]), (right_half_image2.shape[1], right_half_image2.shape[0]))  # Green channel
        
        # Display the images
        plt.figure(figsize=(5, 5))
        plt.imshow(blended_image)
        plt.title('Red/Green Overlay of Shifted and Original Image Halves')
        plt.axis('off')
        plt.savefig("Autofocus/transform/overlap.png")
        self.overlap_image = QPixmap("Autofocus/transform/overlap.png")
        self.img_overlap.setPixmap(self.plot_bf)
        # plt.show()
        ##################################################################################################################################
        
        ##THE RES OF THE CODE WILL FIND THE MATRIX TRANSFORM THAT RELATES THE CAMER XY PLANE AND THE STAGE XY PLANE
        ## YOU MUST ENTER THE STAGE X AND Y VALUES THAT RESULTRED IN THE MOVEMENT BETWEEN THE TWO IMAGES
        # stage_shift_x = 200 # I HAVE JUST GUESSED HERE
        # stage_shift_Y = 200
        
        # Constants: Already known from prior calculations
        a = actual_shift_x / stage_shift_x
        c = actual_shift_y / stage_shift_x
        
        # Calculate theta and M (I.E. ROTATION BETWEEN PLANES AND SCALING FACTOR TO RELATE PIXELS TO MIROMETERS)
        theta = np.arctan2(c, a)
        M = a / np.cos(theta)  # Use cos since a is associated with cos(theta)
        
        # Calculate b and d using theta and M
        b = -M * np.sin(theta)
        d = M * np.cos(theta)
        
        # Print results
        print(f"Rotation (theta): {np.degrees(theta)} degrees")
        print(f"Scaling (M): {M}")
        print(f"Transformation matrix: [[{a:.2f}, {b:.2f}], [{c:.2f}, {d:.2f}]]")
        
        ###############################################################################################################
        #FINALLY WE CAN NOW USE THE INVERSE OF THAT MATRIX TO CALUCLATED THE STAGE MOVEMENT TO RELATE TO ANY DESIRED PIXEL MOVEMENT
        
        # Function to predict stage movements (if needed)
        def predict_stage_movement(px, py):
            T_inv = np.linalg.inv(np.array([[a, b], [c, d]]))
            return T_inv.dot(np.array([px, py]))
        
        # Example use of prediction function
        px_shift, py_shift = 100, 50  # Example pixel shifts
        stage_movement = predict_stage_movement(px_shift, py_shift)
        print(f"Stage X movement: {stage_movement[0]:.2f} um, Stage Y movement: {stage_movement[1]:.2f} um")

