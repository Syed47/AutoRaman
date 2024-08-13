from PyQt5.QtWidgets import QHBoxLayout, QFrame, QLabel, QLineEdit, QPushButton, QRadioButton
from PyQt5.QtGui import QPixmap

from components.tab import Tab
from components.state import state_manager
from core.autofocus import Autofocus, Amplitude, Phase
from core.microscope import microscope

import matplotlib.pyplot as plt
from io import BytesIO


class AutofocusTab(Tab):
    def __init__(self, logger=None):
        super().__init__(logger)
        self.zfocus = None
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
        left_panel.setFixedSize(320, 540)

        line_label1 = QLabel("Start (μm):", left_panel)
        line_label1.setGeometry(40, 20, 100, 40)
        line_label1.setStyleSheet("QLabel { border: none; font-size:16px; };")
        self.txt_start = QLineEdit(left_panel)
        self.txt_start.setPlaceholderText("1350 (μm)")
        self.txt_start.setText("1330")
        self.txt_start.setStyleSheet("QLineEdit { font-size:16px; };")
        self.txt_start.setGeometry(160, 20, 100, 40)

        line_label2 = QLabel("End (μm):", left_panel)
        line_label2.setGeometry(40, 80, 100, 40)
        line_label2.setStyleSheet("QLabel { border: none; font-size:16px; };")
        self.txt_end = QLineEdit(left_panel)
        self.txt_end.setPlaceholderText("1370 (μm)")
        self.txt_end.setText("1370")
        self.txt_end.setStyleSheet("QLineEdit { font-size:16px; };")
        self.txt_end.setGeometry(160, 80, 100, 40)

        line_label3 = QLabel("Step (μm):", left_panel)
        line_label3.setGeometry(40, 140, 100, 40)
        line_label3.setStyleSheet("QLabel { border: none; font-size:16px; };")
        self.txt_step = QLineEdit(left_panel)
        self.txt_step.setPlaceholderText("1 (μm)")
        self.txt_step.setText("2")
        self.txt_step.setStyleSheet("QLineEdit { font-size:16px; };")
        self.txt_step.setGeometry(160, 140, 100, 40)

        line_separator = QFrame(left_panel)
        line_separator.setGeometry(0, 200, 400, 1)
        line_separator.setFrameShape(QFrame.HLine)
        line_separator.setFrameShadow(QFrame.Sunken)

        radio_label = QLabel("Autofocus Strategy:", left_panel)
        radio_label.setGeometry(20, 240, 140, 40)
        radio_label.setStyleSheet("QLabel { border: none; font-size:16px; };")
        self.radio_amplitude = QRadioButton("Amplitude", left_panel)
        self.radio_amplitude.setChecked(True)
        self.radio_amplitude.setGeometry(160, 220, 140, 40)
        self.radio_phase = QRadioButton("Phase", left_panel)
        self.radio_phase.setGeometry(160, 260, 140, 40)

        line_separator2 = QFrame(left_panel)
        line_separator2.setGeometry(0, 320, 400, 1)
        line_separator2.setFrameShape(QFrame.HLine)
        line_separator2.setFrameShadow(QFrame.Sunken)

        self.btn_run = QPushButton("Run", left_panel)
        self.btn_run.setGeometry(20, 360, 280, 40)

        line_separator2 = QFrame(left_panel)
        line_separator2.setGeometry(0, 440, 400, 1)
        line_separator2.setFrameShape(QFrame.HLine)
        line_separator2.setFrameShadow(QFrame.Sunken)

        self.txt_zfocus = QLineEdit(left_panel)
        self.txt_zfocus.setPlaceholderText("z-distance result (μm)")
        self.txt_zfocus.setText("001")
        self.txt_zfocus.setStyleSheet("QLineEdit { font-size:16px; };")
        self.txt_zfocus.setGeometry(60, 470, 200, 40)
        self.txt_zfocus.setReadOnly(True)

        right_panel = QFrame()
        right_panel.setStyleSheet("QFrame { border: 1px solid #444444; };")
        right_panel.setFixedSize(420, 540)

        self.plot_bf = QPixmap("components/image_2.tif")
        self.img_bf = QLabel(right_panel)
        self.img_bf.setStyleSheet("QLabel { border: 1px solid #444444; border-radius: 0px; };")
        self.img_bf.setPixmap(self.plot_bf)
        self.img_bf.setFixedSize(380, 260)
        self.img_bf.setGeometry(20, 5, 380, 260)
        self.img_bf.setScaledContents(True)

        self.plot_var = QPixmap("components/bar.png")
        self.img_var = QLabel(right_panel)
        self.img_var.setStyleSheet("QLabel { border: 1px solid #444444; border-radius: 0px; };")
        self.img_var.setPixmap(self.plot_var)
        self.img_var.setFixedSize(380, 260)
        self.img_var.setGeometry(20, 275, 380, 260)
        self.img_var.setScaledContents(True)

        frame_tab_layout.addWidget(left_panel)
        frame_tab_layout.addWidget(right_panel)
        frame_tab.setLayout(frame_tab_layout)

        tab_layout.addWidget(frame_tab)
        self.setLayout(tab_layout)

    def connect_signals(self):
        self.btn_run.clicked.connect(self.start_autofocus)

    def variance_plot(self):
        variance = microscope.focus_strategy.capture_scores
        path = "Autofocus/plots/variance.png"
        plt.bar(list(range(len(variance))), variance, color='blue', edgecolor='black')
        plt.xticks(list(range(len(variance))))
        plt.title('Image Variance')
        plt.xlabel('Image')
        plt.ylabel('Variance')
        plt.savefig(path)
        return path

    def start_autofocus(self):
        self.preprocess()
        self.logger.log("autofocus")
        try:
            start = float(self.txt_start.text())
            end = float(self.txt_end.text())
            step = float(self.txt_step.text())
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

        if not amplitude and not phase:
            self.logger.log("Error: No autofocus strategy selected.")
            return

        zfocus = None
        if amplitude:
            zfocus = microscope.auto_focus(Amplitude, start, end, step)
        elif phase:
            zfocus = microscope.auto_focus(Phase, start, end, step)

        if zfocus is not None:
            self.logger.log(f"Autofocus Distance: {zfocus}")
            self.zfocus = zfocus
            self.txt_zfocus.setText(str(self.zfocus))
            
            state_manager.set('ZFOCUS', self.zfocus)

            self.plot_bf = QPixmap(microscope.focus_strategy.focused_image)
            self.img_bf.setPixmap(self.plot_bf)

            self.variance_plot()
            self.plot_var = QPixmap(self.variance_plot())
            self.img_var.setPixmap(self.plot_var)
        else:
            self.logger.log("Error: Autofocus failed. Please check the settings and try again.")
        self.postprocess()
