from PyQt5.QtWidgets import QApplication, QFileDialog, QWidget, QHBoxLayout, QGridLayout, QVBoxLayout, QFrame, QSlider, QCheckBox, QComboBox, QLabel, QLineEdit, QPushButton
from PyQt5.QtGui import QPixmap, QCursor
from PyQt5.QtCore import Qt

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
        self.stage_to_camera_width = -338
        self.stage_to_camera_height = -1
        self.init_ui()
        self.connect_signals()
        os.makedirs(f"Autofocus/transform", exist_ok=True)

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

        radio_label = QLabel("Shift X (μm):", left_panel)
        radio_label.setGeometry(40, 60, 140, 40)
        radio_label.setStyleSheet("QLabel { border: none; font-size:16px; };")
        self.txt_shift_x = QLineEdit(left_panel)
        self.txt_shift_x.setText(f"{self.stage_to_camera_width}")
        self.txt_shift_x.setStyleSheet("QLineEdit { font-size:16px; };")
        self.txt_shift_x.setGeometry(160, 60, 100, 40)

        line_label1 = QLabel("Shift Y (μm):", left_panel)
        line_label1.setGeometry(40, 120, 100, 40)
        line_label1.setStyleSheet("QLabel { border: none; font-size:16px; };")
        self.txt_shift_y = QLineEdit(left_panel)
        self.txt_shift_y.setText(f"{self.stage_to_camera_height}")
        self.txt_shift_y.setStyleSheet("QLineEdit { font-size:16px; };")
        self.txt_shift_y.setGeometry(160, 120, 100, 40)

        line_separator2 = QFrame(left_panel)
        line_separator2.setGeometry(0, 180, 400, 1)
        line_separator2.setFrameShape(QFrame.HLine)
        line_separator2.setFrameShadow(QFrame.Sunken)

        line_label2 = QLabel("Pixel Shift X:", left_panel)
        line_label2.setGeometry(40, 200, 100, 40)
        line_label2.setStyleSheet("QLabel { border: none; font-size:16px; };")
        self.txt_pixel_shift_x = QLineEdit(left_panel)
        self.txt_pixel_shift_x.setText("200")
        self.txt_pixel_shift_x.setStyleSheet("QLineEdit { font-size:16px; };")
        self.txt_pixel_shift_x.setGeometry(160, 200, 100, 40)

        line_label3 = QLabel("Pixel Shift Y:", left_panel)
        line_label3.setGeometry(40, 260, 100, 40)
        line_label3.setStyleSheet("QLabel { border: none; font-size:16px; };")
        self.txt_pixel_shift_y = QLineEdit(left_panel)
        self.txt_pixel_shift_y.setText("100")
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
        self.img_overlap.setGeometry(110, 275, 200, 260)
        self.img_overlap.setScaledContents(True)

        frame_tab_layout.addWidget(left_panel)
        frame_tab_layout.addWidget(right_panel)
        frame_tab.setLayout(frame_tab_layout)

        tab_layout.addWidget(frame_tab)
        self.setLayout(tab_layout)
    
    def connect_signals(self):
        self.btn_run.clicked.connect(self.handle_transform)
        self.checkbox_shift.clicked.connect(self.handle_manual_shift)
        self.txt_shift_x.textChanged.connect(self.handle_stage_shift)
        self.txt_shift_x.textChanged.connect(self.handle_stage_shift)

    def preprocess(self):
        state_manager.set('LAMP', True)
        microscope.stage.move(microscope.stage.x, microscope.stage.y, state_manager.get('ZFOCUS'))

    def postprocess(self):
        state_manager.set('LAMP', False)
        microscope.stage.move(microscope.stage.x - self.stage_to_camera_width, 
                              microscope.stage.y - self.stage_to_camera_height, 
                              state_manager.get('ZFOCUS'))

    def update(self):
        pass

    def handle_manual_shift(self):
        checked = self.checkbox_shift.isChecked()
        self.txt_shift_x.setEnabled(checked)
        self.txt_shift_y.setEnabled(checked)
    
    def handle_stage_shift(self):
        stage_x = self.txt_stage_x.text()
        stage_y = self.txt_stage_y.text()

        if stage_x.isdigit():
            self.stage_to_camera_width = int(stage_x) * -1
        elif stage_y.isdigit():
            self.stage_to_camera_height = int(stage_y) * -1
        else:
            self.logger.log("Not a valid stage position value")        

    def handle_transform(self):
        QApplication.setOverrideCursor(QCursor(Qt.WaitCursor))
        self.transform()
        QApplication.restoreOverrideCursor()

    def transform(self):
        self.preprocess()

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

        self.postprocess()

