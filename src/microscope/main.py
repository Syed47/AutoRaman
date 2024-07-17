import sys
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QSizePolicy, QSplitter, QWidget, QVBoxLayout, QHBoxLayout, QFrame, QLabel, QCheckBox, QLineEdit, QTextEdit, QPushButton, QRadioButton, QTabWidget
from PyQt5.QtGui import QPixmap

from style import style_sheet



class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("AutoRaman")
        self.setGeometry(100, 100, 840, 640)

        main_layout = QHBoxLayout(self)

        tab_widget = QTabWidget()
        tab_widget.setStyleSheet(style_sheet)
        tab_widget.setFixedSize(800, 610)
        tab_widget.addTab(self.settings_tab_init(), 'Settings')
        
        (tab_autofocus,
        txt_start,
        txt_end,
        txt_step,
        radio_amplitude,
        radio_phase,
        btn_run,
        plot_variance,
        plot_brighfield) = self.autofocus_tab_init()
        tab_widget.addTab(tab_autofocus, 'Autofocus')

        (tab_laser,
        txt_start, 
        txt_end, 
        txt_step, 
        txt_offset, 
        checkbox_offset, 
        btn_run, 
        plot_variance, 
        plot_laser, 
        txt_x, 
        txt_y, 
        txt_z) = self.laser_tab_init()

        tab_widget.addTab(tab_laser, 'Laser')
        tab_widget.addTab(self.cells_tab_init(), 'Cells')
        tab_widget.addTab(self.spectra_tab_init(), 'Spectra')
        tab_widget.addTab(self.repeat_tab_init(), 'Repeat')
        tab_widget.addTab(self.optimise_tab_init(), 'Optimise')

        log_widget = QWidget()
        log_layout = QVBoxLayout()
        log_widget.setLayout(log_layout)

        self.log_console = QTextEdit()
        self.log_console.setReadOnly(True)
        self.log_console.hide()

        self.collapse_button = QPushButton(">>")
        self.collapse_button.setFixedSize(25, 25)
        self.collapse_button.setCheckable(True)
        self.collapse_button.toggled.connect(self.toggle_log_console)

        log_layout.addWidget(self.collapse_button, alignment=Qt.AlignCenter)
        log_layout.addWidget(self.log_console)

        main_layout.addWidget(tab_widget)
        main_layout.addWidget(log_widget)

        self.setLayout(main_layout)

    def toggle_log_console(self, checked):
        if checked:
            self.log_console.show()
            self.collapse_button.setText("<<")
            self.setFixedSize(1040, 640)
        else:
            self.log_console.hide()
            self.collapse_button.setText(">>")
            self.setFixedSize(860, 640)

    def settings_tab_init(self):
        tab = QWidget()
        tab_layout = QVBoxLayout()
        tab_layout.addWidget(QLabel(f"This is Settings"))
        tab.setLayout(tab_layout)
        return tab

    def autofocus_tab_init(self):
        tab_autofocus = QWidget()
        tab_autofocus.setStyleSheet(style_sheet)
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
        txt_start = QLineEdit(left_panel)
        txt_start.setPlaceholderText("1350 (μm)")
        txt_start.setStyleSheet("QLineEdit { font-size:16px; };")
        txt_start.setGeometry(160, 20, 100, 40)

        line_label2 = QLabel("End (μm):", left_panel)
        line_label2.setGeometry(40, 80, 100, 40)
        line_label2.setStyleSheet("QLabel { border: none; font-size:16px; };")
        txt_end = QLineEdit(left_panel)
        txt_end.setPlaceholderText("1400 (μm)")
        txt_end.setStyleSheet("QLineEdit { font-size:16px; };")
        txt_end.setGeometry(160, 80, 100, 40)

        line_label3 = QLabel("Step (μm):", left_panel)
        line_label3.setGeometry(40, 140, 100, 40)
        line_label3.setStyleSheet("QLabel { border: none; font-size:16px; };")
        txt_step = QLineEdit(left_panel)
        txt_step.setPlaceholderText("1 (μm)")
        txt_step.setStyleSheet("QLineEdit { font-size:16px; };")
        txt_step.setGeometry(160, 140, 100, 40)
        
        line_separator = QFrame(left_panel)
        line_separator.setGeometry(0, 200, 400, 1)
        line_separator.setFrameShape(QFrame.HLine)
        line_separator.setFrameShadow(QFrame.Sunken)
        
        radio_label = QLabel("Autofocus Strategy:", left_panel)
        radio_label.setGeometry(20, 240, 140, 40)
        radio_label.setStyleSheet("QLabel { border: none; font-size:16px; };")
        radio_amplitude = QRadioButton("Amplitude", left_panel)
        radio_amplitude.setChecked(True)
        radio_amplitude.setGeometry(160, 220, 180, 40)
        radio_phase = QRadioButton("Phase", left_panel)
        radio_phase.setGeometry(160, 260, 180, 40)
        
        line_separator2 = QFrame(left_panel)
        line_separator2.setGeometry(0, 320, 400, 1)
        line_separator2.setFrameShape(QFrame.HLine)
        line_separator2.setFrameShadow(QFrame.Sunken)

        btn_run = QPushButton("Run", left_panel)
        btn_run.setGeometry(20, 360, 280, 40)
        
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

        plot_variance = QPixmap("../../Autofocus/image_2.tif")
        image_label1 = QLabel(right_panel)
        image_label1.setStyleSheet("QLabel { border: 1px solid gray; border-radius: 0px; };")
        image_label1.setPixmap(plot_variance)
        image_label1.setFixedSize(380, 260)
        image_label1.setGeometry(20, 5, 380, 260)
        image_label1.setScaledContents(True)  

        plot_brighfield = QPixmap("bar.png")
        image_label2 = QLabel(right_panel)
        image_label2.setStyleSheet("QLabel { border: 1px solid gray; border-radius: 0px; };")
        image_label2.setPixmap(plot_brighfield)
        image_label2.setFixedSize(380, 260)
        image_label2.setGeometry(20, 275, 380, 260)
        image_label2.setScaledContents(True)  

        frame_tab_layout.addWidget(left_panel)
        frame_tab_layout.addWidget(right_panel)
        frame_tab.setLayout(frame_tab_layout)

        tab_layout.addWidget(frame_tab)
        tab_autofocus.setLayout(tab_layout)
        
        return (tab_autofocus,
                txt_start, 
                txt_end, 
                txt_step, 
                radio_amplitude, 
                radio_phase, 
                btn_run,
                plot_variance,
                plot_brighfield)


    def laser_tab_init(self):
        tab_laser = QWidget()
        tab_laser.setStyleSheet(style_sheet)
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
        txt_start = QLineEdit(left_panel)
        txt_start.setPlaceholderText("1350 (μm)")
        txt_start.setStyleSheet("QLineEdit { font-size:16px; };")
        txt_start.setGeometry(160, 20, 100, 40)

        line_label2 = QLabel("End (μm):", left_panel)
        line_label2.setGeometry(40, 80, 100, 40)
        line_label2.setStyleSheet("QLabel { border: none; font-size:16px; };")
        txt_end = QLineEdit(left_panel)
        txt_end.setPlaceholderText("1400 (μm)")
        txt_end.setStyleSheet("QLineEdit { font-size:16px; };")
        txt_end.setGeometry(160, 80, 100, 40)

        line_label3 = QLabel("Step (μm):", left_panel)
        line_label3.setGeometry(40, 140, 100, 40)
        line_label3.setStyleSheet("QLabel { border: none; font-size:16px; };")
        txt_step = QLineEdit(left_panel)
        txt_step.setPlaceholderText("1 (μm)")
        txt_step.setStyleSheet("QLineEdit { font-size:16px; };")
        txt_step.setGeometry(160, 140, 100, 40)
        
        line_separator = QFrame(left_panel)
        line_separator.setGeometry(0, 200, 400, 1)
        line_separator.setFrameShape(QFrame.HLine)
        line_separator.setFrameShadow(QFrame.Sunken)
        
        radio_label = QLabel("Laser Offset:", left_panel)
        radio_label.setGeometry(40, 240, 140, 40)
        radio_label.setStyleSheet("QLabel { border: none; font-size:16px; };")
        txt_offset = QLineEdit(left_panel)
        txt_offset.setPlaceholderText("10 (μm)")
        txt_offset.setStyleSheet("QLineEdit { font-size:16px; };")
        txt_offset.setGeometry(160, 240, 100, 40)
        txt_offset.setReadOnly(True)
        checkbox_offset = QCheckBox("Edit", left_panel)
        checkbox_offset.setGeometry(140, 200, 180, 40)
        checkbox_offset.clicked.connect(lambda: line_edit4.setReadOnly(not check_box.isChecked()))
        
        line_separator2 = QFrame(left_panel)
        line_separator2.setGeometry(0, 300, 400, 1)
        line_separator2.setFrameShape(QFrame.HLine)
        line_separator2.setFrameShadow(QFrame.Sunken)

        btn_run = QPushButton("Run", left_panel)
        btn_run.setGeometry(20, 320, 280, 40)
        
        line_separator2 = QFrame(left_panel)
        line_separator2.setGeometry(0, 380, 400, 1)
        line_separator2.setFrameShape(QFrame.HLine)
        line_separator2.setFrameShadow(QFrame.Sunken)

        line_x = QLabel("X (μm):", left_panel)
        line_x.setGeometry(40, 390, 100, 40)
        line_x.setStyleSheet("QLabel { border: none; font-size:16px; };")
        txt_x = QLineEdit(left_panel)
        txt_x.setPlaceholderText("320 (μm)")
        txt_x.setStyleSheet("QLineEdit { font-size:16px; };")
        txt_x.setGeometry(160, 390, 100, 40)
        txt_x.setReadOnly(True)

        line_label_y = QLabel("Y (μm):", left_panel)
        line_label_y.setGeometry(40, 440, 100, 40)
        line_label_y.setStyleSheet("QLabel { border: none; font-size:16px; };")
        txt_y = QLineEdit(left_panel)
        txt_y.setPlaceholderText("450 (μm)")
        txt_y.setStyleSheet("QLineEdit { font-size:16px; };")
        txt_y.setGeometry(160, 440, 100, 40)
        txt_y.setReadOnly(True)

        line_label_z = QLabel("Z (μm):", left_panel)
        line_label_z.setGeometry(40, 490, 100, 40)
        line_label_z.setStyleSheet("QLabel { border: none; font-size:16px; };")
        txt_z = QLineEdit(left_panel)
        txt_z.setPlaceholderText("1370 (μm)")
        txt_z.setStyleSheet("QLineEdit { font-size:16px; };")
        txt_z.setGeometry(160, 490, 100, 40)
        txt_z.setReadOnly(True)

        right_panel = QFrame()
        right_panel.setStyleSheet("QFrame { border: 1px solid gray; };")  
        right_panel.setFixedSize(420, 540)

        plot_variance = QPixmap("../../Autofocus/image_2.tif")
        image_label1 = QLabel(right_panel)
        image_label1.setStyleSheet("QLabel { border: 1px solid gray; border-radius: 0px; };")
        image_label1.setPixmap(plot_variance)
        image_label1.setFixedSize(380, 260)
        image_label1.setGeometry(20, 5, 380, 260)
        image_label1.setScaledContents(True)  

        plot_laser = QPixmap("bar.png")
        image_label2 = QLabel(right_panel)
        image_label2.setStyleSheet("QLabel { border: 1px solid gray; border-radius: 0px; };")
        image_label2.setPixmap(plot_laser)
        image_label2.setFixedSize(380, 260)
        image_label2.setGeometry(20, 275, 380, 260)
        image_label2.setScaledContents(True)  

        frame_tab_layout.addWidget(left_panel)
        frame_tab_layout.addWidget(right_panel)
        frame_tab.setLayout(frame_tab_layout)

        tab_layout.addWidget(frame_tab)
        tab_laser.setLayout(tab_layout)

        return (tab_laser,
                txt_start, 
                txt_end, 
                txt_step, 
                txt_offset, 
                checkbox_offset, 
                btn_run, 
                plot_variance, 
                plot_laser, 
                txt_x, 
                txt_y, 
                txt_z)

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
