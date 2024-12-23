from PyQt5.QtWidgets import QApplication, QHBoxLayout, QFrame, QLabel, QLineEdit, QPushButton, QRadioButton
from PyQt5.QtGui import QPixmap, QCursor
from PyQt5.QtCore import Qt

from components.tab import Tab
from components.state import state_manager
from core.autofocus import Amplitude, Phase, Manual
from core.microscope import microscope

import matplotlib.pyplot as plt
import os
import re


class AutofocusTab(Tab):
    def __init__(self, logger=None):
        super().__init__(logger)
        self.init_ui()
        self.connect_signals()

    def preprocess(self):
        state_manager.set('LAMP', True)

    def postprocess(self):
        state_manager.set('LAMP', False)

    def init_ui(self):
        tab_layout = QHBoxLayout()

        frame_tab = QFrame()
        frame_tab.setFrameShape(QFrame.StyledPanel)
        frame_tab_layout = QHBoxLayout()

        left_panel = QFrame()
        left_panel.setStyleSheet("QFrame { border: 1px solid #444444; };")
        left_panel.setFixedSize(300, 540)

        line_label1 = QLabel("Start (μm):", left_panel)
        line_label1.setGeometry(40, 20, 100, 40)
        line_label1.setStyleSheet("QLabel { border: none; font-size:16px; };")
        self.txt_start = QLineEdit(left_panel)
        self.txt_start.setPlaceholderText("1350 (μm)")
        self.txt_start.setText(str(state_manager.get('ZSTART')))
        self.txt_start.setStyleSheet("QLineEdit { font-size:16px; };")
        self.txt_start.setGeometry(160, 20, 100, 40)

        line_label2 = QLabel("End (μm):", left_panel)
        line_label2.setGeometry(40, 80, 100, 40)
        line_label2.setStyleSheet("QLabel { border: none; font-size:16px; };")
        self.txt_end = QLineEdit(left_panel)
        self.txt_end.setPlaceholderText("1370 (μm)")
        self.txt_end.setText(str(state_manager.get('ZEND')))
        self.txt_end.setStyleSheet("QLineEdit { font-size:16px; };")
        self.txt_end.setGeometry(160, 80, 100, 40)

        line_label3 = QLabel("Step (μm):", left_panel)
        line_label3.setGeometry(40, 140, 100, 40)
        line_label3.setStyleSheet("QLabel { border: none; font-size:16px; };")
        self.txt_step = QLineEdit(left_panel)
        self.txt_step.setPlaceholderText("1 (μm)")
        self.txt_step.setText(str(state_manager.get('ZSTEP')))
        self.txt_step.setStyleSheet("QLineEdit { font-size:16px; };")
        self.txt_step.setGeometry(160, 140, 100, 40)

        line_separator = QFrame(left_panel)
        line_separator.setGeometry(0, 200, 400, 1)
        line_separator.setFrameShape(QFrame.HLine)
        line_separator.setFrameShadow(QFrame.Sunken)

        radio_label = QLabel("Strategy:", left_panel)
        radio_label.setGeometry(40, 240, 140, 40)
        radio_label.setStyleSheet("QLabel { border: none; font-size:16px; };")
        self.radio_amplitude = QRadioButton("Amplitude", left_panel)
        self.radio_amplitude.setChecked(True)
        self.radio_amplitude.setGeometry(140, 210, 140, 40)
        self.radio_phase = QRadioButton("Phase", left_panel)
        self.radio_phase.setGeometry(140, 250, 140, 40)
        self.radio_manual = QRadioButton("Manual", left_panel)
        self.radio_manual.setGeometry(140, 290, 140, 40)


        line_separator2 = QFrame(left_panel)
        line_separator2.setGeometry(0, 340, 400, 1)
        line_separator2.setFrameShape(QFrame.HLine)
        line_separator2.setFrameShadow(QFrame.Sunken)

        self.btn_run = QPushButton("Run", left_panel)
        self.btn_run.setGeometry(70, 370, 160, 40)

        line_separator2 = QFrame(left_panel)
        line_separator2.setGeometry(0, 440, 400, 1)
        line_separator2.setFrameShape(QFrame.HLine)
        line_separator2.setFrameShadow(QFrame.Sunken)


        line_label_z = QLabel("Z (μm):", left_panel)
        line_label_z.setGeometry(40, 470, 100, 40)
        line_label_z.setStyleSheet("QLabel { border: none; font-size:16px; };")

        self.txt_zfocus = QLineEdit(left_panel)
        self.txt_zfocus.setPlaceholderText("1370 (μm)")
        self.txt_zfocus.setStyleSheet("QLineEdit { font-size:16px; };")
        self.txt_zfocus.setGeometry(160, 470, 100, 40)
        self.txt_zfocus.setReadOnly(True)

        right_panel = QFrame()
        right_panel.setStyleSheet("QFrame { border: 1px solid #444444; };")
        right_panel.setFixedSize(440, 560)

        self.plot_bf = QPixmap("components/microscope.png")
        self.img_bf = QLabel(right_panel)
        # self.img_bf.setStyleSheet("QLabel { border: 1px solid #444444; border-radius: 0px; };")
        self.img_bf.setPixmap(self.plot_bf)
        self.img_bf.setFixedSize(420, 280)
        self.img_bf.setGeometry(10, 0, 420, 280)
        self.img_bf.setScaledContents(True)

        self.plot_var = QPixmap("components/bar-chart.png")
        self.img_var = QLabel(right_panel)
        # self.img_var.setStyleSheet("QLabel { border: 1px solid #444444; border-radius: 0px; };")
        self.img_var.setPixmap(self.plot_var)
        self.img_var.setFixedSize(420, 280)
        self.img_var.setGeometry(10, 280, 420, 280)
        self.img_var.setScaledContents(True)

        frame_tab_layout.addWidget(left_panel)
        frame_tab_layout.addWidget(right_panel)
        frame_tab.setLayout(frame_tab_layout)

        tab_layout.addWidget(frame_tab)
        self.setLayout(tab_layout)

    def connect_signals(self):
        self.btn_run.clicked.connect(self.handle_autofocus)
        self.txt_start.textChanged.connect(lambda val: state_manager.set('ZSTART', (int(val) if val.isdigit() else 1000) ))
        self.txt_end.textChanged.connect(lambda val: state_manager.set('ZEND', (int(val) if val.isdigit() else 1000)))
        self.txt_step.textChanged.connect(lambda val: state_manager.set('ZSTEP', (int(val) if val.isdigit() else 1)))
    
    def handle_variance_plot(self, path="Autofocus/plots/variance.png"):
        variance = microscope.focus_strategy.capture_scores
        plt.bar(list(range(len(variance))), variance, color='blue', edgecolor='black')
        plt.xticks(list(range(len(variance))), rotation=45)
        plt.title('Image Variance')
        plt.xlabel('Image')
        plt.ylabel('Variance')
        plt.savefig(path)
        plt.close()
        self.plot_var = QPixmap(path)
        self.img_var.setPixmap(self.plot_var)
        self.img_bf.repaint()

    def handle_capture_image(self, capture_path):
        self.plot_bf = QPixmap(capture_path)
        self.img_bf.setPixmap(self.plot_bf)
        self.img_bf.repaint()

    # def handle_brightfield_image(self, capture_path, focus):
    #     fig, ax = plt.subplots()
    #     img = mpimg.imread(capture_path)
    #     ax.imshow(img)
    #     ax.legend(['Example Legend'], loc='best', fontsize='large')
    #     ax.set_title('Image Title', fontsize='large')
    #     ax.axis('off')
    #     fig.savefig("Autofocus/plots/brightfield.png")
    #     pixmap = QPixmap.fromImage("Autofocus/plots/brightfield.png")
    #     self.img_bf.setPixmap(pixmap)
    #     self.img_bf.repaint()
        
    def handle_autofocus(self):
        QApplication.setOverrideCursor(QCursor(Qt.WaitCursor))
        self.start_autofocus()
        QApplication.restoreOverrideCursor()        

    def handle_manual_focus(self):
        snapped_image = state_manager.get("SNAPPED-IMAGE")
        if snapped_image is None:
            return None, None
        match = re.search(r'_(\d+).tif$', snapped_image)  
        if match:
            zvalue = match.group(1)
            return snapped_image, int(zvalue) 
        return None, None    

    def start_autofocus(self):
        self.preprocess()
        self.logger.log("autofocus")

        try:
            start = state_manager.get('ZSTART')
            end = state_manager.get('ZEND')
            step = state_manager.get('ZSTEP')
        except ValueError:
            self.logger.log("Error: Invalid input for start, end, or step. Please enter numeric values.")
            return

        if start >= end:
            self.logger.log("Error: Start value must be less than end value.")
            return

        if step <= 0:
            self.logger.log("Error: Step value must be greater than zero.")
            return

        amplitude = self.radio_amplitude.isChecked()
        phase = self.radio_phase.isChecked()
        manual = self.radio_manual.isChecked()

        if not amplitude and not phase and not manual:
            self.logger.log("Error: No autofocus strategy selected.")
            return

        zfocus = None
        if amplitude:
            zfocus = microscope.auto_focus(Amplitude, start, end, step, self.handle_capture_image)
        elif phase:
            zfocus = microscope.auto_focus(Phase, start, end, step, self.handle_capture_image)
        elif manual:
            zfocus = microscope.auto_focus(Manual, 0, 0, 0, self.handle_manual_focus)

        if zfocus is not None:
            self.logger.log(f"Autofocus Distance: {zfocus}")
            self.txt_zfocus.setText(str(zfocus))
            
            state_manager.set('ZFOCUS', zfocus)

            print(">>> focusedImage", microscope.focus_strategy.focused_image)
            self.handle_capture_image(microscope.focus_strategy.focused_image)
            if not manual:
                self.handle_variance_plot()
        else:
            self.logger.log("Error: Autofocus failed. Please check the settings and try again.")
        self.postprocess()

    def update(self):
        self.txt_start.setText(str(state_manager.get('ZSTART')))
        self.txt_end.setText(str(state_manager.get('ZEND')))
        self.txt_step.setText(str(state_manager.get('ZSTEP')))