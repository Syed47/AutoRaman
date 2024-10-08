from PyQt5.QtWidgets import QMessageBox, QFileDialog, QWidget, QHBoxLayout, QGridLayout, QFrame, QSlider, QCheckBox, QComboBox, QLabel, QLineEdit, QPushButton
from PyQt5.QtGui import QPixmap, QImage, QIcon
from PyQt5.QtCore import Qt, QTimer, QSize

from components.tab import Tab
from core.microscope import microscope
from core.controller import controller
from components.state import state_manager

from numpy import max
from time import sleep

import cv2
import matplotlib.pyplot as plt
import tifffile as tiff

class SettingsTab(Tab):
    def __init__(self, logger=None):
        super().__init__(logger)
        self.last_tagged_image = None
        self.snaped_image = None
        self.preprocess()
        self.init_ui()
        self.connect_signals()

    def __del__(self):
        self.postprocess()

    def preprocess(self):
        self.islive = False
        self.xstep = 100
        self.ystep = 100
        self.zstep = 10

    def postprocess(self):
        self.stop_live_view()

    def connect_signals(self):
        self.btn_live.clicked.connect(self.live_preview)
        self.btn_capture.clicked.connect(self.snap_image)
        self.btn_left.clicked.connect(lambda : microscope.move_stage(x=-self.xstep))
        self.btn_right.clicked.connect(lambda : microscope.move_stage(x=self.xstep))
        self.btn_up.clicked.connect(lambda : microscope.move_stage(y=-self.ystep))
        self.btn_down.clicked.connect(lambda : microscope.move_stage(y=self.ystep))
        self.btn_zoom_in.clicked.connect(lambda : microscope.move_stage(z=-self.zstep))
        self.btn_zoom_out.clicked.connect(lambda : microscope.move_stage(z=self.zstep))

        self.config_browse_button.clicked.connect(self.browse_config_file)

        self.slider_exposure.valueChanged.connect(self.change_exposure)
        self.txt_exposure_value.textChanged.connect(lambda text: self.slider_exposure.setValue(int(text) if text.isdigit() else 0))

        self.slider_lamp_voltage.valueChanged.connect(self.change_lamp_voltage)
        self.txt_lamp_voltage_value.textChanged.connect(lambda text: self.slider_lamp_voltage.setValue(int(text) if text.isdigit() else 0))

        self.slider_laser_intensity.valueChanged.connect(self.change_laser_intensity)
        self.txt_laser_intensity_value.textChanged.connect(lambda text: self.slider_laser_intensity.setValue(int(text) if text.isdigit() else 0))
        
        self.cmb_binning.currentIndexChanged.connect(self.set_binning)
        self.cmd_pixel_type.currentIndexChanged.connect(self.set_pixel_type)
        self.cmb_filter_position.currentIndexChanged.connect(self.set_filter_position)

        self.checkbox_lamp_switch.stateChanged.connect(self.handle_lamp_switch)
        self.checkbox_auto_exposure.stateChanged.connect(self.handle_auto_exposure)
        self.checkbox_inverted_image.stateChanged.connect(self.handle_inverted_image)
        self.checkbox_laser_switch.stateChanged.connect(self.handle_laser_switch)

        self.txt_move_x.textChanged.connect(
            lambda value: setattr(self, 'xstep', int(value) if value and int(value) <= 200 else 200)
        )
        self.txt_move_y.textChanged.connect(
            lambda value: setattr(self, 'ystep', int(value) if value and int(value) <= 200 else 200)
        )
        self.txt_move_z.textChanged.connect(
            lambda value: setattr(self, 'zstep', int(value) if value and int(value) <= 200 else 200)
        )

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
        self.cmb_binning.setCurrentText(state_manager.get('BINNING'))

        line_label2 = QLabel("Pixel Type:", left_panel)
        line_label2.setGeometry(40, 160, 100, 40)
        line_label2.setStyleSheet("QLabel { border: none; font-size:16px; };")

        self.cmd_pixel_type = QComboBox(left_panel)
        self.cmd_pixel_type.addItems(["GREY8", "RGB32"])
        self.cmd_pixel_type.setStyleSheet("QComboBox { font-size:16px; };")
        self.cmd_pixel_type.setGeometry(160, 160, 100, 40)
        self.cmd_pixel_type.setCurrentText(state_manager.get('PIXEL-TYPE'))

        line_label3 = QLabel("Filter Position:", left_panel)
        line_label3.setGeometry(40, 220, 100, 40)
        line_label3.setStyleSheet("QLabel { border: none; font-size:16px; };")

        self.cmb_filter_position = QComboBox(left_panel)
        self.cmb_filter_position.addItems(["Position-1", "Position-2", "Position-3", "Position-4", "Position-5", "Position-6"])
        self.cmb_filter_position.setStyleSheet("QComboBox { font-size:16px; };")
        self.cmb_filter_position.setGeometry(160, 220, 100, 40)
        self.cmb_filter_position.setCurrentText(state_manager.get('FILTER-POSITION'))
        
        line_separator = QFrame(left_panel)
        line_separator.setGeometry(0, 280, 400, 1)
        line_separator.setFrameShape(QFrame.HLine)
        line_separator.setFrameShadow(QFrame.Sunken)

        label_exposure = QLabel("Exposure", left_panel)
        label_exposure.setGeometry(5, 300, 100, 40)
        label_exposure.setAlignment(Qt.AlignCenter)
        label_exposure.setStyleSheet("QLabel { border: none; font-size:16px; };")

        self.slider_exposure = QSlider(Qt.Horizontal, left_panel)
        self.slider_exposure.setGeometry(135, 300, 100, 40)
        self.slider_exposure.setMinimum(1)
        self.slider_exposure.setMaximum(2000)
        self.slider_exposure.setValue(50)
        self.slider_exposure.setTickPosition(QSlider.TicksBelow)  
        self.slider_exposure.setTickInterval(50)

        self.txt_exposure_value = QLineEdit(left_panel)
        self.txt_exposure_value.setText("15")
        self.txt_exposure_value.setStyleSheet("QLineEdit { font-size:16px; };")
        self.txt_exposure_value.setGeometry(250, 300, 60, 40)

        label_lamp_voltage = QLabel("Lamp Voltage", left_panel)
        label_lamp_voltage.setGeometry(20, 350, 100, 40)
        label_lamp_voltage.setAlignment(Qt.AlignCenter)
        label_lamp_voltage.setStyleSheet("QLabel { border: none; font-size:16px; };")

        self.slider_lamp_voltage = QSlider(Qt.Horizontal, left_panel)
        self.slider_lamp_voltage.setGeometry(135, 350, 100, 40)
        self.slider_lamp_voltage.setMinimum(0)
        self.slider_lamp_voltage.setMaximum(12)
        self.slider_lamp_voltage.setValue(state_manager.get('LAMP-VOLTAGE'))
        self.slider_lamp_voltage.setTickPosition(QSlider.TicksBelow)  
        self.slider_lamp_voltage.setTickInterval(1)

        self.txt_lamp_voltage_value = QLineEdit(left_panel)
        self.txt_lamp_voltage_value.setText(str(state_manager.get('LAMP-VOLTAGE')))
        self.txt_lamp_voltage_value.setStyleSheet("QLineEdit { font-size:16px; };")
        self.txt_lamp_voltage_value.setGeometry(250, 350, 60, 40)

        label_laser_intensity = QLabel("Laser Intensity", left_panel)
        label_laser_intensity.setGeometry(20, 400, 105, 40)
        label_laser_intensity.setAlignment(Qt.AlignCenter)
        label_laser_intensity.setStyleSheet("QLabel { border: none; font-size:16px; };")

        self.slider_laser_intensity = QSlider(Qt.Horizontal, left_panel)
        self.slider_laser_intensity.setGeometry(135, 400, 100, 40)
        self.slider_laser_intensity.setMinimum(0)
        self.slider_laser_intensity.setMaximum(100)
        self.slider_laser_intensity.setValue(40)
        self.slider_laser_intensity.setTickPosition(QSlider.TicksBelow)  
        self.slider_laser_intensity.setTickInterval(5)

        self.txt_laser_intensity_value = QLineEdit(left_panel)
        self.txt_laser_intensity_value.setText(str(state_manager.get('LASER-INTENSITY')))
        self.txt_laser_intensity_value.setStyleSheet("QLineEdit { font-size:16px; };")
        self.txt_laser_intensity_value.setGeometry(250, 400, 60, 40)

        line_separator2 = QFrame(left_panel)
        line_separator2.setGeometry(0, 460, 400, 1)
        line_separator2.setFrameShape(QFrame.HLine)
        line_separator2.setFrameShadow(QFrame.Sunken)

        self.checkbox_auto_exposure = QCheckBox("Auto-Exposure", left_panel)
        self.checkbox_auto_exposure.setGeometry(5, 470, 180, 40)

        self.checkbox_inverted_image = QCheckBox("Inverted Image", left_panel)
        self.checkbox_inverted_image.setGeometry(5, 510, 180, 40)

        self.checkbox_lamp_switch = QCheckBox("Lamp", left_panel)
        self.checkbox_lamp_switch.setGeometry(180, 470, 120, 40)

        self.checkbox_laser_switch = QCheckBox("Laser", left_panel)
        self.checkbox_laser_switch.setGeometry(180, 510, 120, 40)

        right_panel = QFrame()
        right_panel.setStyleSheet("QFrame { border: 1px solid #444444; };")

        self.image = QPixmap("components/microscope.png")
        self.live_image = QLabel(right_panel)
        self.live_image.setStyleSheet("QLabel { border: 1px solid #444444; border-radius: 0px; };")
        self.live_image.setPixmap(self.image)
        self.live_image.setFixedSize(432, 301)
        self.live_image.setGeometry(0, 0, 432, 301)
        self.live_image.setScaledContents(True)

        line_separator2 = QFrame(right_panel)
        line_separator2.setGeometry(0, 300, 440, 1)
        line_separator2.setFrameShape(QFrame.HLine)
        line_separator2.setFrameShadow(QFrame.Sunken)

        label_x = QLabel("X step (μm):", right_panel)
        label_x.setGeometry(20, 310, 90, 40)
        label_x.setStyleSheet("QLabel { border: none; font-size:16px; };")

        self.txt_move_x = QLineEdit(right_panel)
        self.txt_move_x.setText(str(self.xstep))
        self.txt_move_x.setStyleSheet("QLineEdit { font-size:16px; };")
        self.txt_move_x.setGeometry(130, 310, 60, 40)

        label_y = QLabel("Y step (μm):", right_panel)
        label_y.setGeometry(20, 355, 90, 40)
        label_y.setStyleSheet("QLabel { border: none; font-size:16px; };")

        self.txt_move_y = QLineEdit(right_panel)
        self.txt_move_y.setText(str(self.ystep))
        self.txt_move_y.setStyleSheet("QLineEdit { font-size:16px; };")
        self.txt_move_y.setGeometry(130, 355, 60, 40)

        label_z = QLabel("Z step (μm):", right_panel)
        label_z.setGeometry(20, 400, 90, 40)
        label_z.setStyleSheet("QLabel { border: none; font-size:16px; };")

        self.txt_move_z = QLineEdit(right_panel)
        self.txt_move_z.setText(str(self.zstep))
        self.txt_move_z.setStyleSheet("QLineEdit { font-size:16px; };")
        self.txt_move_z.setGeometry(130, 400, 60, 40)

        self.label_position_x = QLabel(f"X (μm):    {int(microscope.stage.x)}", right_panel)
        self.label_position_x.setGeometry(20, 450, 180, 40)
        self.label_position_x.setStyleSheet("QLabel { border: none; font-size:16px; };")

        self.label_position_y = QLabel(f"Y (μm):    {int(microscope.stage.y)}", right_panel)
        self.label_position_y.setGeometry(20, 480, 180, 40)
        self.label_position_y.setStyleSheet("QLabel { border: none; font-size:16px; };")

        self.label_position_z = QLabel(f"Z (μm):    {int(microscope.stage.z)}", right_panel)
        self.label_position_z.setGeometry(20, 510, 180, 40)
        self.label_position_z.setStyleSheet("QLabel { border: none; font-size:16px; };")


        line_separator2 = QFrame(right_panel)
        line_separator2.setGeometry(200, 300, 1, 400)
        line_separator2.setFrameShape(QFrame.VLine)
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
        self.btn_zoom_in = QPushButton("+", right_panel)
        self.btn_zoom_in.setFixedSize(40, 40)
        self.btn_zoom_out = QPushButton("-", right_panel)
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
        button_layout_widget.setGeometry(205, 320, 220, 130)
        # button_layout_widget.setStyleSheet(""" QWidget { border: 1px solid #444444; } QPushButton { border: none; }""")
        live_icon = QIcon('components/live.png')
        self.btn_live = QPushButton(" Live", right_panel)
        self.btn_live.setGeometry(210, 490, 100, 40)
        self.btn_live.setIcon(live_icon)
        self.btn_live.setIconSize(QSize(24, 24))

        capture_icon = QIcon('components/camera.png')
        self.btn_capture = QPushButton(" Snap", right_panel)
        self.btn_capture.setGeometry(320, 490, 100, 40)
        self.btn_capture.setIcon(capture_icon)
        self.btn_capture.setIconSize(QSize(24, 24))

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

    def handle_lamp_switch(self):
        state_manager.set('LAMP', self.checkbox_lamp_switch.isChecked())

    def handle_laser_switch(self):
        value = state_manager.get('LASER-INTENSITY') if self.checkbox_laser_switch.isChecked() else 0
        state_manager.set('LASER', value)

    def handle_auto_exposure(self):
        state_manager.set('AUTO-EXPOSURE', self.checkbox_auto_exposure.isChecked())
        if state_manager.get('AUTO-EXPOSURE'):
            self.slider_exposure.setEnabled(False)
            self.txt_exposure_value.setEnabled(False)
        else:
            self.slider_exposure.setEnabled(True) 
            self.txt_exposure_value.setEnabled(True)

    def handle_inverted_image(self):
        state_manager.set('INVERTED-IMAGE', self.checkbox_inverted_image.isChecked())

    def change_exposure(self, value):
        if value < 1 or value > 2000:
            self.logger.log("Error: Exposure must be between 0 and 2000")
            return
        self.txt_exposure_value.setText(str(value))
        state_manager.set('EXPOSURE', value)

    def change_lamp_voltage(self, value):
        if value < 0 or value > 12:
            self.logger.log("Error: Lamp voltage must be between 0 and 12")
            return
        self.txt_lamp_voltage_value.setText(str(value))
        state_manager.set('LAMP-VOLTAGE', value)

    def change_laser_intensity(self, value):
        if value < 0 or value > 100:
            self.logger.log("Error: Laser intensity must be between 0 and 100")
            return
        self.txt_laser_intensity_value.setText(str(value))
        state_manager.set('LASER-INTENSITY', value)        
        state_manager.set('LASER', value)        

    def set_binning(self):
        state_manager.set('BINNING', self.cmb_binning.currentText())

    def set_pixel_type(self):
        state_manager.set('PIXEL-TYPE', self.cmd_pixel_type.currentText())

    def set_filter_position(self):
        state_manager.set('FILTER-POSITION', self.cmb_filter_position.currentText())        

    def snap_image(self):
        image = self.last_tagged_image
        if image is None:
            QMessageBox.information(None, "AutoRaman", "Enable live view to snap image.", QMessageBox.Ok)
            return
        self.stop_live_view()
        qimage = QImage(image.data, image.shape[1], image.shape[0], QImage.Format_Grayscale8)
        pixmap = QPixmap.fromImage(qimage)
        self.live_image.setPixmap(pixmap)
        self.live_image.repaint()
        self.snaped_image = f"Autofocus/snaps/capture_{int(microscope.stage.x)}_{int(microscope.stage.y)}_{int(microscope.stage.z)}.tif"        
        tiff.imsave(self.snaped_image, image)
        self.logger.log("Image snapped")

    def live_preview(self):
        if self.islive:
            self.stop_live_view()
        else:
            self.start_live_view()

    def start_live_view(self):
        self.btn_live.setText(" Stop")
        self.btn_live.setStyleSheet("background-color: #F44336;")
        self.logger.log("live preview started")
        self.islive = True
        controller.start_continuous_sequence_acquisition(0)
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.read_image_buffer)
        self.timer.start(100)

    def stop_live_view(self):
        controller.stop_sequence_acquisition()
        self.islive = False
        self.btn_live.setText(" Live")
        self.btn_live.setStyleSheet("background-color: #4CAF50;")
        self.timer.stop()
        self.image = QPixmap("components/microscope.png")
        self.live_image.setPixmap(self.image)
        self.logger.log("live preview stopped")

    def read_image_buffer(self):
        try:
            remaining_images = controller.get_remaining_image_count()
            if remaining_images > 0:
                tagged_image = controller.get_last_tagged_image()
                image = None

                if state_manager.get('PIXEL-TYPE') == "GREY8":
                    image = tagged_image.pix.reshape(tagged_image.tags['Height'], tagged_image.tags['Width'])
                elif state_manager.get('PIXEL-TYPE') == 'RGB32':
                    image = tagged_image.pix.reshape(3072, 4096)
                    image = cv2.resize(image, (tagged_image.tags['Height'], tagged_image.tags['Width'])) 

                if state_manager.get('INVERTED-IMAGE'):
                    image = max(image) - image

                self.last_tagged_image = image
                qimage = QImage(image.data, image.shape[1], image.shape[0], QImage.Format_Grayscale8)
                pixmap = QPixmap.fromImage(qimage)
                self.live_image.setPixmap(pixmap)

                self.label_position_x.setText(f"X (μm):    {int(microscope.stage.x)}")
                self.label_position_y.setText(f"Y (μm):    {int(microscope.stage.y)}")
                self.label_position_z.setText(f"Z (μm):    {int(microscope.stage.z)}")

            else:
                print("Circular buffer is empty, waiting for images...")
                sleep(0.1)

        except Exception as e:
            print(f"Error retrieving image: {e}")
            sleep(0.5)

        # finally:
        #     self.label_position_x.setText(f"X (μm):    {int(microscope.stage.x)}")
        #     self.label_position_y.setText(f"Y (μm):    {int(microscope.stage.y)}")
        #     self.label_position_z.setText(f"Z (μm):    {int(microscope.stage.z)}")

    def update(self):
        pass