from PyQt5.QtWidgets import QFileDialog, QWidget, QHBoxLayout, QGridLayout, QFrame, QSlider, QCheckBox, QComboBox, QLabel, QLineEdit, QPushButton
from PyQt5.QtGui import QPixmap, QImage
from PyQt5.QtCore import Qt, QTimer

from components.tab import Tab
from core.microscope import microscope
from core.controller import controller

from time import sleep

class SettingsTab(Tab):
    def __init__(self, logger=None):
        super().__init__(logger)
        self.init_ui()
        self.connect_signals()
        self.islive = False
        microscope.camera.set_option("PixelType", "GREY8")

    def connect_signals(self):
        self.btn_live.clicked.connect(self.live_preview)
        self.btn_left.clicked.connect(lambda : microscope.move_stage(x=-100))
        self.btn_right.clicked.connect(lambda : microscope.move_stage(x=100))
        self.btn_up.clicked.connect(lambda : microscope.move_stage(y=-100))
        self.btn_down.clicked.connect(lambda : microscope.move_stage(y=100))
        self.btn_zoom_in.clicked.connect(lambda : microscope.move_stage(z=-100))
        self.btn_zoom_out.clicked.connect(lambda : microscope.move_stage(z=100))

    def init_ui(self):
        tab_layout = QHBoxLayout()

        frame_tab = QFrame()
        frame_tab.setFrameShape(QFrame.StyledPanel)
        frame_tab_layout = QHBoxLayout()

        left_panel = QFrame()
        left_panel.setStyleSheet("QFrame { border: 1px solid #444444; };")
        left_panel.setFixedSize(320, 560)

        self.config_file_path = QLineEdit(left_panel)
        self.config_file_path.setPlaceholderText("Select a config file")
        self.config_file_path.setStyleSheet("QLineEdit { font-size:16px; };")
        self.config_file_path.setGeometry(20, 20, 180, 40)
        self.config_browse_button = QPushButton("Browse", left_panel)
        self.config_browse_button.setGeometry(220, 20, 80, 40)
        self.config_browse_button.clicked.connect(self.browse_config_file)

        line_separator = QFrame(left_panel)
        line_separator.setGeometry(0, 80, 400, 1)
        line_separator.setFrameShape(QFrame.HLine)
        line_separator.setFrameShadow(QFrame.Sunken)

        line_label1 = QLabel("Binning:", left_panel)
        line_label1.setGeometry(40, 100, 100, 40)
        line_label1.setStyleSheet("QLabel { border: none; font-size:16px; };")
        self.cmb_binning = QComboBox(left_panel)
        self.cmb_binning.addItems(["1x1", "2x2", "4x4"])
        self.cmb_binning.setStyleSheet("QComboBox { font-size:16px; };")
        self.cmb_binning.setGeometry(160, 100, 100, 40)

        line_label2 = QLabel("Pixel Type:", left_panel)
        line_label2.setGeometry(40, 160, 100, 40)
        line_label2.setStyleSheet("QLabel { border: none; font-size:16px; };")
        self.cmd_pixel_type = QComboBox(left_panel)
        self.cmd_pixel_type.addItems(["GREY8", "RGB32"])
        self.cmd_pixel_type.setStyleSheet("QComboBox { font-size:16px; };")
        self.cmd_pixel_type.setGeometry(160, 160, 100, 40)

        line_label3 = QLabel("Filter Position:", left_panel)
        line_label3.setGeometry(40, 220, 100, 40)
        line_label3.setStyleSheet("QLabel { border: none; font-size:16px; };")
        self.cmb_filter_position = QComboBox(left_panel)
        self.cmb_filter_position.addItems(["Position-1", "Position-2", "Position-3", "Position-4", "Position-5", "Position-6"])
        self.cmb_filter_position.setStyleSheet("QComboBox { font-size:16px; };")
        self.cmb_filter_position.setGeometry(160, 220, 100, 40)

        line_separator = QFrame(left_panel)
        line_separator.setGeometry(0, 280, 400, 1)
        line_separator.setFrameShape(QFrame.HLine)
        line_separator.setFrameShadow(QFrame.Sunken)

        line_label3 = QLabel("Exposure:", left_panel)
        line_label3.setGeometry(40, 300, 100, 40)
        line_label3.setStyleSheet("QLabel { border: none; font-size:16px; };")
        self.txt_exposure = QLineEdit(left_panel)
        self.txt_exposure.setPlaceholderText("15")
        self.txt_exposure.setStyleSheet("QLineEdit { font-size:16px; };")
        self.txt_exposure.setGeometry(160, 300, 100, 40)

        line_label3 = QLabel("Z-Start:", left_panel)
        line_label3.setGeometry(40, 360, 100, 40)
        line_label3.setStyleSheet("QLabel { border: none; font-size:16px; };")
        self.txt_zstart = QLineEdit(left_panel)
        self.txt_zstart.setPlaceholderText("15")
        self.txt_zstart.setStyleSheet("QLineEdit { font-size:16px; };")
        self.txt_zstart.setGeometry(160, 360, 100, 40)

        line_separator2 = QFrame(left_panel)
        line_separator2.setGeometry(0, 420, 400, 1)
        line_separator2.setFrameShape(QFrame.HLine)
        line_separator2.setFrameShadow(QFrame.Sunken)


        right_panel = QFrame()
        right_panel.setStyleSheet("QFrame { border: 1px solid #444444; };")

        self.image = QPixmap("image_2.tif")
        self.live_image = QLabel(right_panel)
        self.live_image.setStyleSheet("QLabel { border: 1px solid #444444; border-radius: 0px; };")
        self.live_image.setPixmap(self.image)
        self.live_image.setFixedSize(420, 280)
        self.live_image.setGeometry(6, 10, 420, 280)
        self.live_image.setScaledContents(True)

        line_separator2 = QFrame(right_panel)
        line_separator2.setGeometry(0, 300, 440, 1)
        line_separator2.setFrameShape(QFrame.HLine)
        line_separator2.setFrameShadow(QFrame.Sunken)

        button_layout = QGridLayout()
        button_layout.setContentsMargins(0, 0, 0, 0)
        button_layout.setSpacing(0)

        self.btn_up = QPushButton("▲", right_panel)
        self.btn_up.setFixedSize(40, 40)
        self.btn_down = QPushButton("▼", right_panel)
        self.btn_down.setFixedSize(40, 40)
        self.btn_left = QPushButton("◄", right_panel)
        self.btn_left.setFixedSize(40, 40)
        self.btn_right = QPushButton("►", right_panel)
        self.btn_right.setFixedSize(40, 40)
        self.btn_zoom_in = QPushButton("➕", right_panel)
        self.btn_zoom_in.setFixedSize(40, 40)
        self.btn_zoom_out = QPushButton("➖", right_panel)
        self.btn_zoom_out.setFixedSize(40, 40)

        label_z = QLabel("   Z", right_panel)
        label_z.setStyleSheet("QLabel { border: none; font-size:16px; };")

        label_xy = QLabel(" X, Y", right_panel)
        label_xy.setStyleSheet("QLabel { border: none; font-size:16px; };")

        button_layout.addWidget(self.btn_up, 0, 1)
        button_layout.addWidget(self.btn_left, 1, 0)
        button_layout.addWidget(self.btn_down, 2, 1)
        button_layout.addWidget(self.btn_right, 1, 2)
        button_layout.addWidget(self.btn_zoom_in, 0, 4)
        button_layout.addWidget(self.btn_zoom_out, 2, 4)
        button_layout.addWidget(label_xy, 1, 1)
        button_layout.addWidget(label_z, 1, 4)

        dummy_widget = QWidget()
        dummy_widget.setFixedSize(0, 0)
        button_layout.addWidget(dummy_widget, 0, 3)
        button_layout.addWidget(dummy_widget, 1, 3)
        button_layout.addWidget(dummy_widget, 2, 3)

        button_layout_widget = QWidget(right_panel)
        button_layout_widget.setLayout(button_layout)
        button_layout_widget.setGeometry(200, 310, 220, 140)
        button_layout_widget.setStyleSheet(""" QWidget { border: 1px solid #444444; } QPushButton { border: none; }""")

        self.checkbox_aut_exposure = QCheckBox("Auto-Exposure", right_panel)
        self.checkbox_aut_exposure.setGeometry(10, 310, 180, 40)
        # self.checkbox_aut_exposure.setStyleSheet("border: 1px solid #444444;")

        # self.checkbox_inverted = QCheckBox("Inverted Image", right_panel)
        # self.checkbox_inverted.setGeometry(10, 360, 180, 40)
        # self.checkbox_inverted.setStyleSheet("border: 1px solid #444444;")

        label = QLabel("Exposure", right_panel)
        label.setGeometry(15, 360, 80, 40)
        label.setAlignment(Qt.AlignCenter)
        label.setStyleSheet("QLabel { border: none; font-size:16px; };")

        self.slider = QSlider(Qt.Horizontal, right_panel)
        self.slider.setGeometry(100, 360, 80, 40)
        self.slider.setMinimum(0)
        self.slider.setMaximum(10)
        self.slider.setValue(0)
        self.slider.setTickPosition(QSlider.TicksBelow)  
        self.slider.setTickInterval(10) 

        # self.checkbox_lamp = QCheckBox("Lamp", right_panel)
        # self.checkbox_lamp.setGeometry(10, 410, 180, 40)
        # self.checkbox_lamp.setStyleSheet("border: 1px solid #444444;")
        label = QLabel("Lamp", right_panel)
        label.setGeometry(2, 410, 80, 40)
        label.setAlignment(Qt.AlignCenter)
        label.setStyleSheet("QLabel { border: none; font-size:16px; };")

        self.slider = QSlider(Qt.Horizontal, right_panel)
        self.slider.setGeometry(100, 410, 80, 40)
        self.slider.setMinimum(0)
        self.slider.setMaximum(10)
        self.slider.setValue(0)
        self.slider.setTickPosition(QSlider.TicksBelow)  
        self.slider.setTickInterval(10) 

        line_separator2 = QFrame(right_panel)
        line_separator2.setGeometry(0, 460, 440, 1)
        line_separator2.setFrameShape(QFrame.HLine)
        line_separator2.setFrameShadow(QFrame.Sunken)

        self.btn_live = QPushButton("Live Preview", right_panel)
        self.btn_live.setGeometry(75, 490, 280, 40)

        frame_tab_layout.addWidget(left_panel)
        frame_tab_layout.addWidget(right_panel)
        frame_tab.setLayout(frame_tab_layout)

        tab_layout.addWidget(frame_tab)
        self.setLayout(tab_layout)

    def browse_config_file(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        file_name, _ = QFileDialog.getOpenFileName(self, "Select Configuration File", "", "Config Files (*.cfg);;All Files (*)", options=options)
        if file_name:
            self.config_file_path.setText(file_name)

    def live_preview(self):
        if self.islive:
            microscope.lamp.set_off()
            controller.stop_sequence_acquisition()
            self.islive = False
            self.btn_live.setText("Start Live")
            self.logger.log("live preview stoped")
        else:
            microscope.lamp.set_on()
            self.btn_live.setText("Stop Live")
            self.logger.log("live preview started")

            self.islive = True
            controller.start_continuous_sequence_acquisition(0)

            self.timer = QTimer(self)
            self.timer.timeout.connect(self.update_image)
            self.timer.start(100)

    def update_image(self):
        try:
            remaining_images = controller.get_remaining_image_count()
            if remaining_images > 0:
                tagged_image = controller.get_last_tagged_image()
                image = tagged_image.pix.reshape(tagged_image.tags['Height'], tagged_image.tags['Width'])
                qimage = QImage(image.data, image.shape[1], image.shape[0], QImage.Format_Grayscale8)
                pixmap = QPixmap.fromImage(qimage)
                self.live_image.setPixmap(pixmap)
            else:
                print("Circular buffer is empty, waiting for images...")
                sleep(0.1)

        except Exception as e:
            print(f"Error retrieving image: {e}")
            sleep(0.5)
