from PyQt5.QtWidgets import QHBoxLayout, QFrame, QLabel, QLineEdit, QPushButton, QCheckBox, QSlider, QMessageBox
from PyQt5.QtGui import QPixmap, QImage
from PyQt5.QtCore import Qt

from components.tab import Tab
from components.messagebox import MessageBox
from components.state import state_manager
from core.microscope import microscope
from core.base_cell_identifier import CellPose

import os
os.environ['KMP_DUPLICATE_LIB_OK'] = 'True'
import numpy as np
import json
from cellpose import models
from cellpose.io import imread
import matplotlib.pyplot as plt
from scipy.ndimage import center_of_mass


class CellsTab(Tab):
    def __init__(self, logger=None):
        super().__init__(logger)
        self.diameter = 100
        self.threshold = 6 # 0-10 / 10
        self.models = {
            'cyto': False,
            'nuclei': False,
            'custom': False
        }
        self.cellpose = CellPose()
        self.init_ui()
        self.connect_signals()

    def init_ui(self):        
        tab_layout = QHBoxLayout()

        frame_tab = QFrame()
        frame_tab.setFrameShape(QFrame.StyledPanel)
        frame_tab_layout = QHBoxLayout()

        left_panel = QFrame()
        left_panel.setStyleSheet("QFrame { border: 1px solid #444444; };")
        left_panel.setFixedSize(320, 540)

        line_label1 = QLabel("Cell Diameter (px):", left_panel)
        line_label1.setGeometry(20, 20, 160, 40)
        line_label1.setStyleSheet("QLabel { border: none; font-size:16px; };")

        self.txt_diameter = QLineEdit(left_panel)
        self.txt_diameter.setText(str(self.diameter))
        self.txt_diameter.setStyleSheet("QLineEdit { font-size:16px; };")
        self.txt_diameter.setGeometry(200, 20, 100, 40)

        line_label2 = QLabel("Confidence Threshold:", left_panel)
        line_label2.setGeometry(20, 80, 160, 40)
        line_label2.setAlignment(Qt.AlignCenter)
        line_label2.setStyleSheet("QLabel { border: none; font-size:16px; };")

        self.slider_conf_threshold = QSlider(Qt.Horizontal, left_panel)
        self.slider_conf_threshold.setGeometry(200, 80, 100, 40)
        self.slider_conf_threshold.setMinimum(0)
        self.slider_conf_threshold.setMaximum(10)
        self.slider_conf_threshold.setValue(6)
        self.slider_conf_threshold.setTickPosition(QSlider.TicksBelow)  
        self.slider_conf_threshold.setTickInterval(1)

        line_separator = QFrame(left_panel)
        line_separator.setGeometry(0, 140, 400, 1)
        line_separator.setFrameShape(QFrame.HLine)
        line_separator.setFrameShadow(QFrame.Sunken)

        self.checkbox_cyto = QCheckBox("Cellpose - Cyto Model", left_panel)
        # self.checkbox_cyto.setChecked(True)
        self.checkbox_cyto.setGeometry(20, 160, 240, 40)

        self.checkbox_nuclei = QCheckBox("Cellpose - Nuclei Model", left_panel)
        # self.checkbox_nuclei.setChecked(True)
        self.checkbox_nuclei.setGeometry(20, 200, 240, 40)

        self.checkbox_custom = QCheckBox("Peak-Local-Max Model", left_panel)
        self.checkbox_custom.setGeometry(20, 240, 240, 40)

        line_separator2 = QFrame(left_panel)
        line_separator2.setGeometry(0, 300, 400, 1)
        line_separator2.setFrameShape(QFrame.HLine)
        line_separator2.setFrameShadow(QFrame.Sunken)

        self.btn_run = QPushButton("Identify", left_panel)
        self.btn_run.setGeometry(80, 320, 160, 40)

        right_panel = QFrame()
        right_panel.setStyleSheet("QFrame { border: 1px solid #444444; };")
        right_panel.setFixedSize(420, 540)

        self.plot_bf = QPixmap("components/microscope.png")
        self.img_bf = QLabel(right_panel)
        self.img_bf.setStyleSheet("QLabel { border: 1px solid #444444; border-radius: 0px; };")
        self.img_bf.setPixmap(self.plot_bf)
        self.img_bf.setFixedSize(380, 260)
        self.img_bf.setGeometry(20, 5, 380, 260)
        self.img_bf.setScaledContents(True)

        self.plot_seg = QPixmap("components/bar-chart.png")
        self.img_seg = QLabel(right_panel)
        self.img_seg.setStyleSheet("QLabel { border: 1px solid #444444; border-radius: 0px; };")
        self.img_seg.setPixmap(self.plot_seg)
        self.img_seg.setFixedSize(380, 260)
        self.img_seg.setGeometry(20, 275, 380, 260)
        self.img_seg.setScaledContents(True)

        frame_tab_layout.addWidget(left_panel)
        frame_tab_layout.addWidget(right_panel)
        frame_tab.setLayout(frame_tab_layout)

        tab_layout.addWidget(frame_tab)
        self.setLayout(tab_layout)

    def connect_signals(self):
        self.btn_run.clicked.connect(self.identify)
        self.txt_diameter.textChanged.connect(self.set_diameter)
        self.slider_conf_threshold.valueChanged.connect(self.change_conf_threshold)
        self.checkbox_cyto.stateChanged.connect(self.handle_models)
        self.checkbox_nuclei.stateChanged.connect(self.handle_models)
        self.checkbox_custom.stateChanged.connect(self.handle_models)

    def preprocess(self):
        return super().preprocess()
    
    def postprocess(self):
        return super().postprocess()
    
    def update(self):
        return super().update()
    
    def set_diameter(self, val):
        self.diameter = int(val) if val.isdigit() else 100
        self.txt_diameter.setText(str(self.diameter))
        self.logger.log("Diameter:" + str(self.diameter))

    def change_conf_threshold(self, val):
        self.threshold = val / 10
        self.slider_conf_threshold.setValue(val)
        self.logger.log("Threshold:" + str(self.threshold))

    def handle_models(self):
        self.models['cyto'] = self.checkbox_cyto.isChecked()
        self.models['nuclei'] = self.checkbox_nuclei.isChecked()
        self.models['custom'] = self.checkbox_custom.isChecked()
        self.logger.log(json.dumps(self.models, indent=4))

    def identify(self):

        if not self.checkbox_cyto.isChecked() and not self.checkbox_nuclei.isChecked():
            MessageBox(text="Please select at least one checkbox (cytoplasm or nuclei) to proceed.",
                       icon=QMessageBox.Warning)
            return

        if microscope.focus_strategy is None:
            MessageBox(text="Please run the Autofocus routine before continuing.",
                       icon=QMessageBox.Warning)
            return

        input_img = microscope.focus_strategy.focused_image
        output_img = "Autofocus/plots/segmentation.png"

        img = imread(input_img)
        self.plot_bf = QPixmap(input_img)
        self.img_bf.setPixmap(self.plot_bf)

        models = []

        if self.checkbox_cyto.isChecked():
            models.append('cyto')
        if self.checkbox_nuclei.isChecked():
            models.append('nuclei')
        
        cyto_mask, nuclei_mask, nuclei_centre = self.cellpose.identify(img, self.diameter, self.threshold, models)

        plt.imshow(img, cmap='gray')
        
        if cyto_mask is not None:
            plt.imshow(cyto_mask, cmap='jet', alpha=0.5)

        if nuclei_mask is not None:
            plt.imshow(nuclei_mask, cmap='cool', alpha=0.5)
            for nuclei in nuclei_centre:
                plt.plot(nuclei[1], nuclei[0], 'ro', markersize=3)

        plt.axis('off')
        plt.savefig(output_img, bbox_inches='tight', pad_inches=0)
        plt.close()

        self.plot_seg = QPixmap(output_img)
        self.img_seg.setPixmap(self.plot_seg)

