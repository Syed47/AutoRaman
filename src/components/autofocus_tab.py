from PyQt5.QtWidgets import QWidget, QHBoxLayout, QFrame, QLabel, QLineEdit, QPushButton, QRadioButton
from PyQt5.QtGui import QPixmap

from style import style_sheet


class AutofocusTab(QWidget):
    def __init__(self, logger=None):
        super().__init__()
        self.logger = logger
        self.initUI()

    def initUI(self):
        self.create_autofocus_tab()
        self.connect_signals()

    def create_autofocus_tab(self):
        self.tab_autofocus = QWidget()
        self.tab_autofocus.setStyleSheet(style_sheet)
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

        zfocus = QLineEdit(left_panel)
        zfocus.setPlaceholderText("z-distance result (μm)")
        zfocus.setStyleSheet("QLineEdit { font-size:16px; };")
        zfocus.setGeometry(60, 470, 200, 40)
        zfocus.setReadOnly(True)

        right_panel = QFrame()
        right_panel.setStyleSheet("QFrame { border: 1px solid #444444; };")
        right_panel.setFixedSize(420, 540)

        self.plot_variance = QPixmap("image_2.tif")
        image_label1 = QLabel(right_panel)
        image_label1.setStyleSheet("QLabel { border: 1px solid #444444; border-radius: 0px; };")
        image_label1.setPixmap(self.plot_variance)
        image_label1.setFixedSize(380, 260)
        image_label1.setGeometry(20, 5, 380, 260)
        image_label1.setScaledContents(True)

        self.plot_brighfield = QPixmap("bar.png")
        image_label2 = QLabel(right_panel)
        image_label2.setStyleSheet("QLabel { border: 1px solid #444444; border-radius: 0px; };")
        image_label2.setPixmap(self.plot_brighfield)
        image_label2.setFixedSize(380, 260)
        image_label2.setGeometry(20, 275, 380, 260)
        image_label2.setScaledContents(True)

        frame_tab_layout.addWidget(left_panel)
        frame_tab_layout.addWidget(right_panel)
        frame_tab.setLayout(frame_tab_layout)

        tab_layout.addWidget(frame_tab)
        self.tab_autofocus.setLayout(tab_layout)

    def get_widget(self):
        return self.tab_autofocus

    def connect_signals(self):
        self.btn_run.clicked.connect(self.start_autofocus)

    def start_autofocus(self):
        self.logger.log("autofocus")
        return
        try:
            start = float(self.txt_start.text())
            end = float(self.txt_end.text())
            step = float(self.txt_step.text())
        except ValueError:
            self.logger.append("Error: Invalid input for start, end, or step. Please enter numeric values.")
            return

        if start >= end:
            self.logger.append("Error: Start value must be less than end value.")
            return

        if step <= 0:
            self.logger.append("Error: Step value must be greater than zero.")
            return

        amplitude = self.radio_amplitude.isChecked()
        phase = self.radio_phase.isChecked()

        if not amplitude and not phase:
            self.logger.append("Error: No autofocus strategy selected.")
            return

        zfocus = None
        if amplitude:
            zfocus = self.microscope.focus("Amplitude", start, end, step)
        elif phase:
            zfocus = self.microscope.focus("Phase", start, end, step)

        if zfocus is not None:
            self.logger.append(f"Autofocus Distance: {zfocus}")
        else:
            self.logger.append("Error: Autofocus failed. Please check the settings and try again.")