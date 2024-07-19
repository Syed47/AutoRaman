from PyQt5.QtWidgets import QWidget, QHBoxLayout, QFrame, QCheckBox, QComboBox, QLabel, QLineEdit, QPushButton, QRadioButton
from style import style_sheet

class SettingsTab(QWidget):
    def __init__(self, logger=None):
        super().__init__()
        self.logger = logger
        self.initUI()

    def initUI(self):
        self.create_settings_tab()
        self.connect_signals()

    def create_settings_tab(self):
        self.tab_settings = QWidget()
        self.tab_settings.setStyleSheet(style_sheet)
        tab_layout = QHBoxLayout()

        frame_tab = QFrame()
        frame_tab.setFrameShape(QFrame.StyledPanel)
        frame_tab_layout = QHBoxLayout()

        left_panel = QFrame()
        left_panel.setStyleSheet("QFrame { border: 1px solid #444444; };")
        left_panel.setFixedSize(320, 540)

        line_label1 = QLabel("Binning:", left_panel)
        line_label1.setGeometry(40, 20, 100, 40)
        line_label1.setStyleSheet("QLabel { border: none; font-size:16px; };")
        self.cmb_start = QComboBox(left_panel)
        self.cmb_start.addItems(["1x1", "2x2", "4x4"])
        self.cmb_start.setStyleSheet("QComboBox { font-size:16px; };")
        self.cmb_start.setGeometry(160, 20, 100, 40)

        line_label2 = QLabel("Pixel Type:", left_panel)
        line_label2.setGeometry(40, 80, 100, 40)
        line_label2.setStyleSheet("QLabel { border: none; font-size:16px; };")
        self.cmb_end = QComboBox(left_panel)
        self.cmb_end.addItems(["GREY8", "RGB32"])
        self.cmb_end.setStyleSheet("QComboBox { font-size:16px; };")
        self.cmb_end.setGeometry(160, 80, 100, 40)

        line_label3 = QLabel("Filter Position:", left_panel)
        line_label3.setGeometry(40, 140, 100, 40)
        line_label3.setStyleSheet("QLabel { border: none; font-size:16px; };")
        self.cmb_step = QComboBox(left_panel)
        self.cmb_step.addItems(["Position-1", "Position-2", "Position-3", "Position-4", "Position-5", "Position-6"])
        self.cmb_step.setStyleSheet("QComboBox { font-size:16px; };")
        self.cmb_step.setGeometry(160, 140, 100, 40)

        line_separator = QFrame(left_panel)
        line_separator.setGeometry(0, 200, 400, 1)
        line_separator.setFrameShape(QFrame.HLine)
        line_separator.setFrameShadow(QFrame.Sunken)

        line_label3 = QLabel("Exposure:", left_panel)
        line_label3.setGeometry(40, 220, 100, 40)
        line_label3.setStyleSheet("QLabel { border: none; font-size:16px; };")
        self.txt_step = QLineEdit(left_panel)
        self.txt_step.setPlaceholderText("15")
        self.txt_step.setStyleSheet("QLineEdit { font-size:16px; };")
        self.txt_step.setGeometry(160, 220, 100, 40)

        line_separator2 = QFrame(left_panel)
        line_separator2.setGeometry(0, 280, 400, 1)
        line_separator2.setFrameShape(QFrame.HLine)
        line_separator2.setFrameShadow(QFrame.Sunken)

        self.checkbox_aut_exposure = QCheckBox("Auto-Exposure", left_panel)
        self.checkbox_aut_exposure.setGeometry(80, 300, 180, 40)

        self.checkbox_inverted = QCheckBox("Inverted Image", left_panel)
        self.checkbox_inverted.setGeometry(80, 340, 180, 40)

        self.checkbox_lamp = QCheckBox("Lamp", left_panel)
        self.checkbox_lamp.setGeometry(80, 380, 180, 40)

        line_separator2 = QFrame(left_panel)
        line_separator2.setGeometry(0, 440, 400, 1)
        line_separator2.setFrameShape(QFrame.HLine)
        line_separator2.setFrameShadow(QFrame.Sunken)

        self.btn_apply = QPushButton("Apply", left_panel)
        self.btn_apply.setGeometry(20, 470, 280, 40)

        frame_tab_layout.addWidget(left_panel)
        frame_tab.setLayout(frame_tab_layout)

        tab_layout.addWidget(frame_tab)
        self.tab_settings.setLayout(tab_layout)

    def get_widget(self):
        return self.tab_settings

    def connect_signals(self):
        self.btn_apply.clicked.connect(self.apply_settings)

    def apply_settings(self):
        self.logger.log("settings applied")
        return
