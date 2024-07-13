
import sys
from PyQt5.QtWidgets import QApplication, QSizePolicy, QWidget, QVBoxLayout, QHBoxLayout, QFrame, QLabel, QCheckBox, QLineEdit, QPushButton, QRadioButton, QTabWidget
from PyQt5.QtGui import QPixmap

from style import style_sheet

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("AutoRaman")
        self.setGeometry(100, 100, 840, 640)
        self.setFixedSize(840, 640)
        
        main_layout = QHBoxLayout()
        tab_widget = QTabWidget()
        tab_widget.setStyleSheet(style_sheet)

        tab_widget.addTab(self.settings_tab_init(), 'Settings')
        tab_widget.addTab(self.autofocus_tab_init(), 'Autofocus')
        tab_widget.addTab(self.laser_tab_init(), 'Laser')
        tab_widget.addTab(self.cells_tab_init(), 'Cells')
        tab_widget.addTab(self.spectra_tab_init(), 'Spectra')
        tab_widget.addTab(self.repeat_tab_init(), 'Repeat')
        tab_widget.addTab(self.optimise_tab_init(), 'Optimise')
        
        main_layout.addWidget(tab_widget)

        self.setLayout(main_layout)


    def settings_tab_init(self):
        tab = QWidget()
        tab_layout = QVBoxLayout()
        tab_layout.addWidget(QLabel(f"This is Settings"))
        tab.setLayout(tab_layout)
        return tab

    def autofocus_tab_init(self):
        tab = QWidget()
        tab.setStyleSheet(style_sheet)
        tab_layout = QHBoxLayout()
        
        frame_tab = QFrame()
        frame_tab.setFrameShape(QFrame.StyledPanel)
        frame_tab_layout = QHBoxLayout()
        
        left_panel = QFrame()
        left_panel.setStyleSheet("QFrame { border: 1px solid gray; };")  
        left_panel.setFixedSize(320, 540)
        
        line_label1 = QLabel("Start (μm):", left_panel)
        line_label1.setGeometry(40, 20, 100, 40)
        line_label1.setStyleSheet("QLabel { border: none; font-size:16px; };")
        line_edit1 = QLineEdit(left_panel)
        line_edit1.setPlaceholderText("1350 (μm)")
        line_edit1.setStyleSheet("QLineEdit { font-size:16px; };")
        line_edit1.setGeometry(160, 20, 100, 40)

        line_label2 = QLabel("End (μm):", left_panel)
        line_label2.setGeometry(40, 80, 100, 40)
        line_label2.setStyleSheet("QLabel { border: none; font-size:16px; };")
        line_edit2 = QLineEdit(left_panel)
        line_edit2.setPlaceholderText("1400 (μm)")
        line_edit2.setStyleSheet("QLineEdit { font-size:16px; };")
        line_edit2.setGeometry(160, 80, 100, 40)

        line_label3 = QLabel("Step (μm):", left_panel)
        line_label3.setGeometry(40, 140, 100, 40)
        line_label3.setStyleSheet("QLabel { border: none; font-size:16px; };")
        line_edit3 = QLineEdit(left_panel)
        line_edit3.setPlaceholderText("1 (μm)")
        line_edit3.setStyleSheet("QLineEdit { font-size:16px; };")
        line_edit3.setGeometry(160, 140, 100, 40)
        
        line_separator = QFrame(left_panel)
        line_separator.setGeometry(0, 200, 400, 1)
        line_separator.setFrameShape(QFrame.HLine)
        line_separator.setFrameShadow(QFrame.Sunken)
        
        radio_label = QLabel("Autofocus Strategy:", left_panel)
        radio_label.setGeometry(20, 240, 140, 40)
        radio_label.setStyleSheet("QLabel { border: none; font-size:16px; };")
        radio_button1 = QRadioButton("Amplitude", left_panel)
        radio_button1.setChecked(True)
        radio_button1.setGeometry(160, 220, 180, 40)
        radio_button2 = QRadioButton("Phase", left_panel)
        radio_button2.setGeometry(160, 260, 180, 40)
        
        line_separator2 = QFrame(left_panel)
        line_separator2.setGeometry(0, 320, 400, 1)
        line_separator2.setFrameShape(QFrame.HLine)
        line_separator2.setFrameShadow(QFrame.Sunken)

        run_button = QPushButton("Run", left_panel)
        run_button.setGeometry(20, 360, 280, 40)
        
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
        right_panel.setStyleSheet("QFrame { border: 1px solid gray; };")  
        right_panel.setFixedSize(420, 540)

        pixmap1 = QPixmap("../../Autofocus/image_2.tif")
        image_label1 = QLabel(right_panel)
        image_label1.setStyleSheet("QLabel { border: 1px solid gray; border-radius: 0px; };")
        image_label1.setPixmap(pixmap1)
        image_label1.setFixedSize(380, 260)
        image_label1.setGeometry(20, 5, 380, 260)
        image_label1.setScaledContents(True)  

        pixmap2 = QPixmap("bar.png")
        image_label2 = QLabel(right_panel)
        image_label2.setStyleSheet("QLabel { border: 1px solid gray; border-radius: 0px; };")
        image_label2.setPixmap(pixmap2)
        image_label2.setFixedSize(380, 260)
        image_label2.setGeometry(20, 275, 380, 260)
        image_label2.setScaledContents(True)  

        frame_tab_layout.addWidget(left_panel)
        frame_tab_layout.addWidget(right_panel)
        frame_tab.setLayout(frame_tab_layout)

        tab_layout.addWidget(frame_tab)
        tab.setLayout(tab_layout)

        return tab

    def laser_tab_init(self):
        tab = QWidget()
        tab.setStyleSheet(style_sheet)
        tab_layout = QHBoxLayout()
        
        frame_tab = QFrame()
        frame_tab.setFrameShape(QFrame.StyledPanel)
        frame_tab_layout = QHBoxLayout()
        
        left_panel = QFrame()
        left_panel.setStyleSheet("QFrame { border: 1px solid gray; };")  
        left_panel.setFixedSize(320, 540)
        
        line_label1 = QLabel("Start (μm):", left_panel)
        line_label1.setGeometry(40, 20, 100, 40)
        line_label1.setStyleSheet("QLabel { border: none; font-size:16px; };")
        line_edit1 = QLineEdit(left_panel)
        line_edit1.setPlaceholderText("1350 (μm)")
        line_edit1.setStyleSheet("QLineEdit { font-size:16px; };")
        line_edit1.setGeometry(160, 20, 100, 40)

        line_label2 = QLabel("End (μm):", left_panel)
        line_label2.setGeometry(40, 80, 100, 40)
        line_label2.setStyleSheet("QLabel { border: none; font-size:16px; };")
        line_edit2 = QLineEdit(left_panel)
        line_edit2.setPlaceholderText("1400 (μm)")
        line_edit2.setStyleSheet("QLineEdit { font-size:16px; };")
        line_edit2.setGeometry(160, 80, 100, 40)

        line_label3 = QLabel("Step (μm):", left_panel)
        line_label3.setGeometry(40, 140, 100, 40)
        line_label3.setStyleSheet("QLabel { border: none; font-size:16px; };")
        line_edit3 = QLineEdit(left_panel)
        line_edit3.setPlaceholderText("1 (μm)")
        line_edit3.setStyleSheet("QLineEdit { font-size:16px; };")
        line_edit3.setGeometry(160, 140, 100, 40)
        
        line_separator = QFrame(left_panel)
        line_separator.setGeometry(0, 200, 400, 1)
        line_separator.setFrameShape(QFrame.HLine)
        line_separator.setFrameShadow(QFrame.Sunken)
        
        radio_label = QLabel("Laser Offset:", left_panel)
        radio_label.setGeometry(40, 240, 140, 40)
        radio_label.setStyleSheet("QLabel { border: none; font-size:16px; };")
        line_edit4 = QLineEdit(left_panel)
        line_edit4.setPlaceholderText("10 (μm)")
        line_edit4.setStyleSheet("QLineEdit { font-size:16px; };")
        line_edit4.setGeometry(160, 240, 100, 40)
        line_edit4.setReadOnly(True)
        check_box = QCheckBox("Edit", left_panel)
        check_box.setGeometry(140, 200, 180, 40)
        check_box.clicked.connect(lambda: line_edit4.setReadOnly(not check_box.isChecked()))

        
        line_separator2 = QFrame(left_panel)
        line_separator2.setGeometry(0, 300, 400, 1)
        line_separator2.setFrameShape(QFrame.HLine)
        line_separator2.setFrameShadow(QFrame.Sunken)

        run_button = QPushButton("Run", left_panel)
        run_button.setGeometry(20, 320, 280, 40)
        
        line_separator2 = QFrame(left_panel)
        line_separator2.setGeometry(0, 380, 400, 1)
        line_separator2.setFrameShape(QFrame.HLine)
        line_separator2.setFrameShadow(QFrame.Sunken)

        line_x = QLabel("X (μm):", left_panel)
        line_x.setGeometry(40, 390, 100, 40)
        line_x.setStyleSheet("QLabel { border: none; font-size:16px; };")
        line_edit_x = QLineEdit(left_panel)
        line_edit_x.setPlaceholderText("320 (μm)")
        line_edit_x.setStyleSheet("QLineEdit { font-size:16px; };")
        line_edit_x.setGeometry(160, 390, 100, 40)
        line_edit_x.setReadOnly(True)

        line_label_y = QLabel("Y (μm):", left_panel)
        line_label_y.setGeometry(40, 440, 100, 40)
        line_label_y.setStyleSheet("QLabel { border: none; font-size:16px; };")
        line_edit_y = QLineEdit(left_panel)
        line_edit_y.setPlaceholderText("450 (μm)")
        line_edit_y.setStyleSheet("QLineEdit { font-size:16px; };")
        line_edit_y.setGeometry(160, 440, 100, 40)
        line_edit_y.setReadOnly(True)

        line_label_z = QLabel("Z (μm):", left_panel)
        line_label_z.setGeometry(40, 490, 100, 40)
        line_label_z.setStyleSheet("QLabel { border: none; font-size:16px; };")
        line_edit_z = QLineEdit(left_panel)
        line_edit_z.setPlaceholderText("1370 (μm)")
        line_edit_z.setStyleSheet("QLineEdit { font-size:16px; };")
        line_edit_z.setGeometry(160, 490, 100, 40)
        line_edit_z.setReadOnly(True)

        right_panel = QFrame()
        right_panel.setStyleSheet("QFrame { border: 1px solid gray; };")  
        right_panel.setFixedSize(420, 540)

        pixmap1 = QPixmap("../../Autofocus/image_2.tif")
        image_label1 = QLabel(right_panel)
        image_label1.setStyleSheet("QLabel { border: 1px solid gray; border-radius: 0px; };")
        image_label1.setPixmap(pixmap1)
        image_label1.setFixedSize(380, 260)
        image_label1.setGeometry(20, 5, 380, 260)
        image_label1.setScaledContents(True)  

        pixmap2 = QPixmap("bar.png")
        image_label2 = QLabel(right_panel)
        image_label2.setStyleSheet("QLabel { border: 1px solid gray; border-radius: 0px; };")
        image_label2.setPixmap(pixmap2)
        image_label2.setFixedSize(380, 260)
        image_label2.setGeometry(20, 275, 380, 260)
        image_label2.setScaledContents(True)  

        frame_tab_layout.addWidget(left_panel)
        frame_tab_layout.addWidget(right_panel)
        frame_tab.setLayout(frame_tab_layout)

        tab_layout.addWidget(frame_tab)
        tab.setLayout(tab_layout)

        return tab

    def cells_tab_init(self):
        tab = QWidget()
        tab_layout = QVBoxLayout()
        tab_layout.addWidget(QLabel(f"This is Cells"))
        tab.setLayout(tab_layout)
        return tab

    def spectra_tab_init(self):
        tab = QWidget()
        tab_layout = QVBoxLayout()
        tab_layout.addWidget(QLabel(f"This is Spectra"))
        tab.setLayout(tab_layout)
        return tab

    def repeat_tab_init(self):
        tab = QWidget()
        tab_layout = QVBoxLayout()
        tab_layout.addWidget(QLabel(f"This is Repeat"))
        tab.setLayout(tab_layout)
        return tab

    def optimise_tab_init(self):
        tab = QWidget()
        tab_layout = QVBoxLayout()
        tab_layout.addWidget(QLabel(f"This is Optimise"))
        tab.setLayout(tab_layout)
        return tab



if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
