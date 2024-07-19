from PyQt5.QtWidgets import QWidget, QHBoxLayout, QFrame, QLabel, QCheckBox, QLineEdit, QPushButton
from PyQt5.QtGui import QPixmap

from style import style_sheet

class LaserTab(QWidget):
    def __init__(self, logger=None):
        super().__init__()
        self.logger = logger
        self.initUI()
        self.connect_signals()

    def initUI(self):
        self.tab_laser = QWidget()
        self.tab_laser.setStyleSheet(style_sheet)
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
        self.checkbox_offset.clicked.connect(lambda: self.txt_offset.setReadOnly(not self.checkbox_offset.isChecked()))
        
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

        self.plot_variance = QPixmap("image_2.tif")
        image_label1 = QLabel(right_panel)
        image_label1.setStyleSheet("QLabel { border: 1px solid #444444; border-radius: 0px; };")
        image_label1.setPixmap(self.plot_variance)
        image_label1.setFixedSize(380, 260)
        image_label1.setGeometry(20, 5, 380, 260)
        image_label1.setScaledContents(True)  

        self.plot_laser = QPixmap("bar.png")
        image_label2 = QLabel(right_panel)
        image_label2.setStyleSheet("QLabel { border: 1px solid #444444; border-radius: 0px; };")
        image_label2.setPixmap(self.plot_laser)
        image_label2.setFixedSize(380, 260)
        image_label2.setGeometry(20, 275, 380, 260)
        image_label2.setScaledContents(True)  

        frame_tab_layout.addWidget(left_panel)
        frame_tab_layout.addWidget(right_panel)
        frame_tab.setLayout(frame_tab_layout)

        tab_layout.addWidget(frame_tab)
        self.tab_laser.setLayout(tab_layout)

    def get_widget(self):
        return self.tab_laser

    def connect_signals(self):
        self.btn_run.clicked.connect(self.start_laser_focus)

    def start_laser_focus(self):
        self.logger.log("autofocus laser")
        return