from PyQt5.QtWidgets import QApplication, QHBoxLayout, QFrame, QLabel, QLineEdit, QPushButton, QCheckBox, QSlider, QMessageBox
from PyQt5.QtGui import QPixmap, QCursor, QPainter, QColor

from PyQt5.QtCore import Qt, QTimer


import os
from components.tab import Tab
from components.messagebox import MessageBox
from components.state import state_manager
from core.controller import controller
from core.microscope import microscope
from core.camera import CCDCamera, SpectralCamera
os.environ['KMP_DUPLICATE_LIB_OK'] = 'True'
from core.base_cell_identifier import CellPose

import numpy as np
import json
import cv2
from cellpose import models
from cellpose.io import imread
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import tifffile as tiff
from time import sleep
from scipy.ndimage import center_of_mass


class InteractiveImage(QLabel):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.points = []

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            pos = event.pos()
            self.points.append(pos)
            self.update() 

    def paintEvent(self, event):
        super().paintEvent(event)
        painter = QPainter(self)
        for index, point in enumerate(self.points, start=1):
            painter.setPen(QColor(255, 0, 0))
            painter.setBrush(QColor(255, 0, 0))
            painter.drawEllipse(point, 2, 2)
            painter.setPen(QColor(0, 255, 0)) 
            painter.drawText(point, str(index))
    

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
        self.live = False
        self.cellpose = CellPose()
        self.last_tagged_image = None
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

        self.checkbox_custom = QCheckBox("Manual Selection", left_panel)
        self.checkbox_custom.setGeometry(20, 240, 240, 40)

        line_separator2 = QFrame(left_panel)
        line_separator2.setGeometry(0, 300, 400, 1)
        line_separator2.setFrameShape(QFrame.HLine)
        line_separator2.setFrameShadow(QFrame.Sunken)

        self.btn_run = QPushButton("Identify", left_panel)
        self.btn_run.setGeometry(80, 320, 160, 40)

        self.btn_spectra = QPushButton("Spectra", left_panel)
        self.btn_spectra.setGeometry(80, 380, 160, 40)

        self.right_panel = QFrame()
        self.right_panel.setStyleSheet("QFrame { border: 1px solid #444444; };")
        self.right_panel.setFixedSize(420, 540)

        self.plot_bf = QPixmap("components/microscope.png")
        self.img_bf = InteractiveImage(self.right_panel)
        self.img_bf.setStyleSheet("QLabel { border: none; border-radius: 0px; };")
        self.img_bf.setPixmap(self.plot_bf)
        self.img_bf.setFixedSize(380, 260)
        self.img_bf.setGeometry(20, 5, 380, 260)
        self.img_bf.setScaledContents(True)

        self.plot_seg = QPixmap("components/bar-chart.png")
        self.img_seg = QLabel(self.right_panel)
        # self.img_seg.setStyleSheet("QLabel { border: 1px solid #444444; border-radius: 0px; };")
        self.img_seg.setPixmap(self.plot_seg)
        self.img_seg.setFixedSize(380, 260)
        self.img_seg.setGeometry(20, 275, 380, 260)
        self.img_seg.setScaledContents(True)

        frame_tab_layout.addWidget(left_panel)
        frame_tab_layout.addWidget(self.right_panel)
        frame_tab.setLayout(frame_tab_layout)

        tab_layout.addWidget(frame_tab)
        self.setLayout(tab_layout)

    def connect_signals(self):
        self.btn_run.clicked.connect(self.handle_identification)
        self.btn_spectra.clicked.connect(self.record_spectra)
        self.txt_diameter.textChanged.connect(self.set_diameter)
        self.slider_conf_threshold.valueChanged.connect(self.change_conf_threshold)
        self.checkbox_cyto.stateChanged.connect(self.handle_models)
        self.checkbox_nuclei.stateChanged.connect(self.handle_models)
        self.checkbox_custom.stateChanged.connect(self.handle_manual_selection)

    def preprocess(self):
        return super().preprocess()
    
    def postprocess(self):
        return super().postprocess()
    
    def update(self):
        pass
        # if self.is_active():
        #     if microscope.focus_strategy is not None:
        #         input_img = microscope.focus_strategy.focused_image
        #         self.plot_bf = QPixmap(input_img)
        #         self.img_bf.setPixmap(self.plot_bf)
        # else:
        #     self.plot_bf = QPixmap("components/microscope.png")
        #     self.img_bf.setPixmap(self.plot_bf)

    def set_diameter(self, val):
        self.diameter = int(val) if val.isdigit() else 100
        self.txt_diameter.setText(str(self.diameter))
        self.logger.log("Diameter:" + str(self.diameter))

    def change_conf_threshold(self, val):
        self.threshold = val / 10
        self.slider_conf_threshold.setValue(val)
        self.logger.log("Threshold:" + str(self.threshold))

    def handle_manual_selection(self):
        image = state_manager.get("SNAPPED-IMAGE")
        if image is not None:
            if self.checkbox_custom.isChecked():
                self.plot_bf = QPixmap(image)
                self.img_bf = InteractiveImage(self.right_panel) 
                self.img_bf.setPixmap(self.plot_bf)
                self.img_bf.setGeometry(20, 5, 380, 260)
                self.img_bf.setFixedSize(380, 260)
                self.img_bf.setScaledContents(True)
                self.img_bf.show()

            self.plot_bf = QPixmap(image)
            self.img_bf.setPixmap(self.plot_bf)
            self.img_bf.repaint()
            self.logger.log(str(self.img_bf.points))
        else:
            self.plot_bf = QPixmap("components/microscope.png")
            self.img_bf.setPixmap(self.plot_bf)
            self.img_bf.repaint()
        
    def handle_models(self):
        self.models['cyto'] = self.checkbox_cyto.isChecked()
        self.models['nuclei'] = self.checkbox_nuclei.isChecked()
        self.models['custom'] = self.checkbox_custom.isChecked()
        self.logger.log(json.dumps(self.models, indent=4))

    def handle_identification(self):
        QApplication.setOverrideCursor(QCursor(Qt.WaitCursor))
        self.identify()
        QApplication.restoreOverrideCursor()

    def handle_spectra(self):
        if self.live:
            self.stop_live_view()
            self.live = False
        else:
            self.start_live_view()
            self.live = True

    def start_live_view(self):
        print("LIVE VIEW STARTED")
        microscope.camera.set_camera('Andor')
        microscope.camera.set_exposure(1000)
        microscope.camera.set_option("ReadMode", "FVB")
        print(microscope.camera.get_property('ReadMode'))
        print(microscope.camera.camera)
        self.logger.log("live preview started")
        controller.start_continuous_sequence_acquisition(0)
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.read_image_buffer)
        self.timer.start(500)

    def stop_live_view(self):
        controller.stop_sequence_acquisition()
        self.timer.stop()
        # self.plot_seg = QPixmap("components/microscope.png")
        # self.img_seg.setPixmap(self.last_tagged_image)
        self.logger.log("live preview stopped")

    def read_image_buffer(self):
        print('READING LIVE IMAGE')
        try:
            remaining_images = controller.get_remaining_image_count()
            if remaining_images > 0:
                tagged_image = controller.get_last_tagged_image()
                image = tagged_image.pix.reshape(tagged_image.tags['Height'], tagged_image.tags['Width'])

                self.last_tagged_image = image
                print("last tagged imaged updated")
            else:
                print("Circular buffer is empty, waiting for images...")
                sleep(0.1)

        except Exception as e:
            print(f"Error retrieving image: {e}")
            sleep(0.5)

    def record_spectra(self):
        state_manager.set('LAMP', False)
        state_manager.set('LASER', 100)
        sleep(2)
        if state_manager.get('LASER-XYZ') is None:
            MessageBox(text="Please run the laser focus routine before continuing.",
                       icon=QMessageBox.Warning)
            return
        plt.clf()
        width, height = microscope.camera.width, microscope.camera.height
        print('Camera XY:', width, height)
        microscope.set_camera(SpectralCamera(exposure=state_manager.get('EXPOSURE-ANDOR')))
        sleep(2)
        Sx, Sy = microscope.stage.x, microscope.stage.y
        X, Y, Z = state_manager.get('LASER-XYZ')
        print(X,Y,Z)
        self.points = [(i+1, p.x(), p.y()) for i, p in enumerate(self.img_bf.points)]
        transform_matrix = state_manager.get('TRANSFORM-MATRIX')
        x_values = np.linspace(0, 1024, 1024)
        # scaled_points = []
        for p in self.points:
            x, y = p[1] * (width / 380) , p[2] * (height / 260)
            dx, dy = X - x, y - Y
            sx, sy = transform_matrix(dx, dy)
            microscope.move_stage(sx, sy)
            sleep(2)
            X, Y = x, y
            image = microscope.camera.capture()
            plt.plot(x_values, image[0], label=str(p[0]))
            # debuging
            # microscope.set_camera(CCDCamera(exposure=state_manager.get('EXPOSURE-AMSCOPE')))
            # # state_manager.set('LAMP', True)
            # sleep(1)
            # image = microscope.snap_image()
            # if len(image.shape) > 2:
            #     image = np.mean(image, axis=-1) 
            # ly, lx = np.unravel_index(np.argmax(image), image.shape)
            # scaled_points.append((x, y, lx, ly))
            # microscope.set_camera(SpectralCamera(exposure=state_manager.get('EXPOSURE-ANDOR')))
            # state_manager.set('LAMP', False)
            # # state_manager.set('LASER', state_manager.get('LASER-INTENSITY'))
            # sleep(1)

        plt.legend()
        plt.savefig("Autofocus/plots/spectra.png", bbox_inches='tight', pad_inches=0)
        plt.close()

        self.plot_seg = QPixmap("Autofocus/plots/spectra.png")
        self.img_seg.setPixmap(self.plot_seg)

        state_manager.set('LASER', 0)

        microscope.set_camera(CCDCamera(exposure=state_manager.get('EXPOSURE-AMSCOPE')))
        # microscope.stage.move(Sx, Sy)
        sleep(1)

        # x, y, lx, ly = zip(*scaled_points)
        # image = tiff.imread(state_manager.get('SNAPPED-IMAGE'))
        # plt.imshow(image)
        # plt.plot(x, y, marker='o', color='g', linestyle='--', linewidth=1, markersize=2)
        # plt.plot(lx, ly, marker='+', color='r', linestyle='None', markersize=2)
        # plt.axis('off') 
        # plt.show()
        # plt.close()




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
        plt.imshow(img, cmap='gray')

        model = []
        if self.checkbox_cyto.isChecked():
            model.append('cyto')
        if self.checkbox_nuclei.isChecked():
            model.append('nuclei')

        cyto, nuclei = self.cellpose.identify(img, self.diameter, self.threshold, model)

        if cyto is not None:
            plt.imshow(cyto, cmap='jet', alpha=0.5)

        if nuclei is not None:
            plt.imshow(nuclei[0], cmap='cool', alpha=0.5)
            for nucleus in nuclei[1]:
                plt.plot(nucleus[1], nucleus[0], 'ro', markersize=3)

        plt.axis('off')
        plt.savefig(output_img, bbox_inches='tight', pad_inches=0)
        plt.close()

        self.plot_seg = QPixmap(output_img)
        self.img_seg.setPixmap(self.plot_seg)


