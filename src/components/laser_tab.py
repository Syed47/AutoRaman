from PyQt5.QtWidgets import QHBoxLayout, QFrame, QLabel, QCheckBox, QLineEdit, QPushButton
from PyQt5.QtGui import QPixmap

from components.tab import Tab
from components.state import state_manager
from core.microscope import microscope
import matplotlib.pyplot as plt
from core.autofocus import Laser

import tifffile as tiff
import numpy as np

class LaserTab(Tab):
    def __init__(self, logger=None):
        super().__init__(logger)
        self.init_ui()
        self.connect_signals()

    def preprocess(self):
        state_manager.set('LAMP', False)
        state_manager.set('LASER', 40)

    def postprocess(self):
        state_manager.set('LASER', 40)

    def init_ui(self):
        tab_layout = QHBoxLayout()
        
        frame_tab = QFrame()
        frame_tab.setFrameShape(QFrame.StyledPanel)
        frame_tab_layout = QHBoxLayout()
        
        left_panel = QFrame()
        left_panel.setStyleSheet("QFrame { border: 1px solid #444444; };")  
        left_panel.setFixedSize(320, 540)
        
        line_label1 = QLabel("Start (μm):", left_panel)
        line_label1.setGeometry(40, 20, 100, 40)
        line_label1.setStyleSheet("QLabel { border: none; font-size:16px; };")
        self.txt_start = QLineEdit(left_panel)
        self.txt_start.setPlaceholderText("1350 (μm)")
        self.txt_start.setStyleSheet("QLineEdit { font-size:16px; };")
        self.txt_start.setGeometry(160, 20, 100, 40)

        line_label2 = QLabel("End (μm):", left_panel)
        line_label2.setGeometry(40, 80, 100, 40)
        line_label2.setStyleSheet("QLabel { border: none; font-size:16px; };")
        self.txt_end = QLineEdit(left_panel)
        self.txt_end.setPlaceholderText("1400 (μm)")
        self.txt_end.setStyleSheet("QLineEdit { font-size:16px; };")
        self.txt_end.setGeometry(160, 80, 100, 40)

        line_label3 = QLabel("Step (μm):", left_panel)
        line_label3.setGeometry(40, 140, 100, 40)
        line_label3.setStyleSheet("QLabel { border: none; font-size:16px; };")
        self.txt_step = QLineEdit(left_panel)
        self.txt_step.setPlaceholderText("1 (μm)")
        self.txt_step.setStyleSheet("QLineEdit { font-size:16px; };")
        self.txt_step.setGeometry(160, 140, 100, 40)
        
        line_separator = QFrame(left_panel)
        line_separator.setGeometry(0, 200, 400, 1)
        line_separator.setFrameShape(QFrame.HLine)
        line_separator.setFrameShadow(QFrame.Sunken)
        
        radio_label = QLabel("Laser Offset:", left_panel)
        radio_label.setGeometry(40, 240, 140, 40)
        radio_label.setStyleSheet("QLabel { border: none; font-size:16px; };")
        self.txt_offset = QLineEdit(left_panel)
        self.txt_offset.setPlaceholderText("10 (μm)")
        self.txt_offset.setStyleSheet("QLineEdit { font-size:16px; };")
        self.txt_offset.setGeometry(160, 245, 100, 40)
        self.txt_offset.setReadOnly(True)
        self.checkbox_offset = QCheckBox("Edit", left_panel)
        self.checkbox_offset.setGeometry(140, 205, 160, 40)
        self.checkbox_offset.setChecked(False)
        
        line_separator2 = QFrame(left_panel)
        line_separator2.setGeometry(0, 300, 400, 1)
        line_separator2.setFrameShape(QFrame.HLine)
        line_separator2.setFrameShadow(QFrame.Sunken)

        self.btn_run = QPushButton("Run", left_panel)
        self.btn_run.setGeometry(20, 320, 280, 40)
        
        line_separator2 = QFrame(left_panel)
        line_separator2.setGeometry(0, 380, 400, 1)
        line_separator2.setFrameShape(QFrame.HLine)
        line_separator2.setFrameShadow(QFrame.Sunken)

        line_x = QLabel("X (μm):", left_panel)
        line_x.setGeometry(40, 390, 100, 40)
        line_x.setStyleSheet("QLabel { border: none; font-size:16px; };")
        self.txt_x = QLineEdit(left_panel)
        self.txt_x.setPlaceholderText("320 (μm)")
        self.txt_x.setStyleSheet("QLineEdit { font-size:16px; };")
        self.txt_x.setGeometry(160, 390, 100, 40)
        self.txt_x.setReadOnly(True)

        line_label_y = QLabel("Y (μm):", left_panel)
        line_label_y.setGeometry(40, 440, 100, 40)
        line_label_y.setStyleSheet("QLabel { border: none; font-size:16px; };")
        self.txt_y = QLineEdit(left_panel)
        self.txt_y.setPlaceholderText("450 (μm)")
        self.txt_y.setStyleSheet("QLineEdit { font-size:16px; };")
        self.txt_y.setGeometry(160, 440, 100, 40)
        self.txt_y.setReadOnly(True)

        line_label_z = QLabel("Z (μm):", left_panel)
        line_label_z.setGeometry(40, 490, 100, 40)
        line_label_z.setStyleSheet("QLabel { border: none; font-size:16px; };")
        self.txt_z = QLineEdit(left_panel)
        self.txt_z.setPlaceholderText("1370 (μm)")
        self.txt_z.setStyleSheet("QLineEdit { font-size:16px; };")
        self.txt_z.setGeometry(160, 490, 100, 40)
        self.txt_z.setReadOnly(True)

        right_panel = QFrame()
        right_panel.setStyleSheet("QFrame { border: 1px solid #444444; };")  
        right_panel.setFixedSize(420, 540)

        self.plot_bf = QPixmap("microscope.png")
        self.img_bf = QLabel(right_panel)
        self.img_bf.setStyleSheet("QLabel { border: 1px solid #444444; border-radius: 0px; };")
        self.img_bf.setPixmap(self.plot_bf)
        self.img_bf.setFixedSize(380, 260)
        self.img_bf.setGeometry(20, 5, 380, 260)
        self.img_bf.setScaledContents(True)

        self.plot_intensity_score = QPixmap("bar-chart.png")
        self.img_var = QLabel(right_panel)
        self.img_var.setStyleSheet("QLabel { border: 1px solid #444444; border-radius: 0px; };")
        self.img_var.setPixmap(self.plot_intensity_score)
        self.img_var.setFixedSize(380, 260)
        self.img_var.setGeometry(20, 275, 380, 260)
        self.img_var.setScaledContents(True)

        frame_tab_layout.addWidget(left_panel)
        frame_tab_layout.addWidget(right_panel)
        frame_tab.setLayout(frame_tab_layout)

        tab_layout.addWidget(frame_tab)
        self.setLayout(tab_layout)

    def connect_signals(self):
        self.btn_run.clicked.connect(self.start_laser_focus)
        self.checkbox_offset.clicked.connect(self.handle_manual_offset)

    def handle_manual_offset(self):
        checked = self.checkbox_offset.isChecked()
        self.txt_offset.setReadOnly(not checked)
        if checked:
            offset_text = self.txt_offset.text()
            if offset_text.isdigit():
                Tab.set_state('LASER-OFFSET', int(offset_text))
            else:
                self.logger.log("Offset value is not a valid number.")

    def plot_intensity_scores(self):
        score = microscope.focus_strategy.capture_scores
        path = "Autofocus/plots/intensity_score.png"
        plt.bar(list(range(len(score))), score, color='blue', edgecolor='black')
        plt.xticks(list(range(len(score))))
        plt.title('Image Scores')
        plt.xlabel('Image')
        plt.ylabel('Intensity Score')
        plt.savefig(path)
        return path

    def handle_capture_image(self, capture_path):
        self.plot_bf = QPixmap(capture_path)
        self.img_bf.setPixmap(self.plot_bf)

    def start_laser_focus(self):
        self.preprocess()
        self.logger.log("laser focus")
        try:
            start = int(self.txt_start.text())
            end = int(self.txt_end.text())
            step = int(self.txt_step.text())
        except ValueError:
            self.logger.log("Error: Invalid input for start, end, or step. Please enter numeric values.")
            return

        if start >= end:
            self.logger.log("Error: Start value must be less than end value.")
            return

        if step <= 0:
            self.logger.log("Error: Step value must be greater than zero.")
            return

        laserfocus = microscope.auto_focus(Laser, start, end, step, self.handle_capture_image)
 
        if laserfocus is not None:
            self.logger.log(f"Laser focus distance: {laserfocus}")
            
            image_array = np.array(tiff.imread(microscope.focus_strategy.focused_image))

            if len(image_array.shape) > 2:
                image_array = np.mean(image_array, axis=-1) 

            y, x = np.unravel_index(np.argmax(image_array), image_array.shape)

            print(f"The best focused image is: {microscope.focus_strategy.focused_image}")
            print(f"Bright spot is at  ({x}, {y})")
            self.txt_x.setText(str(x))
            self.txt_y.setText(str(y))
            self.txt_z.setText(str(laserfocus))
            
            Tab.set_state('LASER-OFFSET', Tab.get_state('ZFOCUS') - laserfocus)
            self.txt_offset.setText(str(Tab.get_state('LASER-OFFSET')))

            self.handle_capture_image(microscope.focus_strategy.focused_image)

            self.plot_intensity_scores()
            self.plot_intensity_score = QPixmap(self.plot_intensity_scores())
            self.img_var.setPixmap(self.plot_intensity_score)
        else:
            self.logger.log("Error: Laser focus failed. Please check the settings and try again.")
        
        self.postprocess()
