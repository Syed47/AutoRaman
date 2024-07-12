
import sys
from PyQt5.QtWidgets import QApplication, QSizePolicy, QWidget, QVBoxLayout, QHBoxLayout, QFrame, QLabel, QLineEdit, QPushButton, QRadioButton, QTabWidget
from PyQt5.QtGui import QPixmap

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("AutoRaman")
        self.setGeometry(100, 100, 800, 600)

        
        main_layout = QHBoxLayout()

        
        tab_widget = QTabWidget()
        tab_widget.setStyleSheet("""
            QTabBar::tab {
                height:24px;
                width: 120px;
                font-size: 14px;
            }
        """)

        
        tab1 = QWidget()
        tab1_layout = QHBoxLayout()

        tab1.setStyleSheet("""
            /* Styling for QPushButton */
            QPushButton {
                background-color: #4CAF50; /* Green background */
                color: white; /* White text */
                border: none; /* No border */
                padding: 10px 20px; /* Padding */
                font-size: 16px; /* Font size */
                border-radius: 8px;
            }
            QPushButton:hover {
                background-color: #45a049; /* Darker green on hover */
            }

            /* Styling for QRadioButton */
            QRadioButton {
                font-size: 16px; /* Font size */
                color: #333; /* Text color */
                spacing: 10px; /* Space between text and indicator */
                padding-left: 20px; /* Space between indicator and text */
                padding-right: 20px; /* Space between text and border */
            }

            /* Styling for QLabel (labels associated with QLineEdit and QRadioButton) */
            QLabel {
                font-size: 14px; /* Larger font size for labels */
            }

            /* Styling for QLineEdit */
            QLineEdit {
                padding: 8px; /* Padding */
                border: 1px solid #ccc; /* Gray border */
                border-radius: 4px; /* Rounded corners */
            }
                           
            QRadioButton::indicator::unchecked {
                border: 2px solid #555; /* Border color of unchecked state */
                background-color: #EEE; /* Background color of unchecked state */
                border-radius: 10px; /* Rounded corners for the indicator */
            }
            QRadioButton::indicator::checked {
                border: 2px solid #555; /* Border color of checked state */
                background-color: #4CAF50; /* Background color of checked state */
                border-radius: 10px; /* Rounded corners for the indicator */
            }      
        """)

        
        frame_tab1 = QFrame()
        frame_tab1.setFrameShape(QFrame.StyledPanel)
        frame_tab1_layout = QHBoxLayout()

        
        left_panel = QFrame()
        left_panel.setStyleSheet("QFrame { border: 1px solid black; border-radius: 4px };")  
        left_panel.setFixedSize(320, 600)

        
        line_label1 = QLabel("Start (μm):", left_panel)
        line_label1.setGeometry(40, 40, 100, 40)
        line_label1.setStyleSheet("QLabel { border: none; font-size:16px; };")
        line_edit1 = QLineEdit(left_panel)
        line_edit1.setPlaceholderText("1350")
        line_edit1.setStyleSheet("QLineEdit { font-size:16px; };")
        line_edit1.setGeometry(160, 40, 100, 40)

        line_label2 = QLabel("End (μm):", left_panel)
        line_label2.setGeometry(40, 100, 100, 40)
        line_label2.setStyleSheet("QLabel { border: none; font-size:16px; };")
        line_edit2 = QLineEdit(left_panel)
        line_edit2.setPlaceholderText("1400")
        line_edit2.setStyleSheet("QLineEdit { font-size:16px; };")
        line_edit2.setGeometry(160, 100, 100, 40)

        line_label3 = QLabel("Step (μm):", left_panel)
        line_label3.setGeometry(40, 160, 100, 40)
        line_label3.setStyleSheet("QLabel { border: none; font-size:16px; };")
        line_edit3 = QLineEdit(left_panel)
        line_edit3.setPlaceholderText("1")
        line_edit3.setStyleSheet("QLineEdit { font-size:16px; };")
        line_edit3.setGeometry(160, 160, 100, 40)

        
        line_separator = QFrame(left_panel)
        line_separator.setGeometry(0, 240, 400, 1)
        line_separator.setFrameShape(QFrame.HLine)
        line_separator.setFrameShadow(QFrame.Sunken)

        
        radio_label = QLabel("Autofocus Strategy:", left_panel)
        radio_label.setGeometry(20, 300, 140, 40)
        radio_label.setStyleSheet("QLabel { border: none; font-size:16px; };")
        radio_button1 = QRadioButton("Amplitude", left_panel)
        radio_button1.setChecked(True)
        radio_button1.setGeometry(160, 280, 180, 40)
        radio_button2 = QRadioButton("Phase", left_panel)
        radio_button2.setGeometry(160, 320, 180, 40)

        
        line_separator2 = QFrame(left_panel)
        line_separator2.setGeometry(0, 400, 400, 1)
        line_separator2.setFrameShape(QFrame.HLine)
        line_separator2.setFrameShadow(QFrame.Sunken)

        run_button = QPushButton("Run", left_panel)
        run_button.setGeometry(20, 440, 280, 40)
        
        line_separator2 = QFrame(left_panel)
        line_separator2.setGeometry(0, 520, 400, 1)
        line_separator2.setFrameShape(QFrame.HLine)
        line_separator2.setFrameShadow(QFrame.Sunken)

        zfocus = QLineEdit(left_panel)
        zfocus.setPlaceholderText("z-distance result (μm)")
        zfocus.setStyleSheet("QLineEdit { font-size:16px; };")
        zfocus.setGeometry(60, 540, 200, 40)
        zfocus.setReadOnly(True)

        
        right_panel = QFrame()
        right_panel.setStyleSheet("QFrame { border: 1px solid black; border-radius: 4px; };")  
        right_panel.setFixedSize(460, 600)

        pixmap1 = QPixmap("../Autofocus/image_2.tif")
        image_label1 = QLabel(right_panel)
        image_label1.setStyleSheet("QLabel { border: 1px solid black; border-radius: 0px; };")
        image_label1.setPixmap(pixmap1)
        image_label1.setFixedSize(400, 280)
        image_label1.setGeometry(30, 10, 400, 280)
        image_label1.setScaledContents(True)  

        pixmap2 = QPixmap("bar.png")
        image_label2 = QLabel(right_panel)
        image_label2.setStyleSheet("QLabel { border: 1px solid black; border-radius: 0px; };")
        image_label2.setPixmap(pixmap2)
        image_label2.setFixedSize(400, 280)
        image_label2.setGeometry(30, 310, 400, 280)
        image_label2.setScaledContents(True)  

        
        frame_tab1_layout.addWidget(left_panel)
        frame_tab1_layout.addWidget(right_panel)
        frame_tab1.setLayout(frame_tab1_layout)

        
        tab1_layout.addWidget(frame_tab1)
        tab1.setLayout(tab1_layout)


        settings = QWidget()
        settings_layout = QVBoxLayout()
        settings_layout.addWidget(QLabel(f"This is settings"))
        settings.setLayout(settings_layout)
        tab_widget.addTab(settings, "Settings")

        tab_widget.addTab(tab1, "Autofocus")

        
        for i in ['Laser', 'Cells', 'Spectra', 'Repeat', 'Optimise']:
            tab = QWidget()
            tab_layout = QVBoxLayout()
            tab_layout.addWidget(QLabel(f"This is Tab {i}"))
            tab.setLayout(tab_layout)
            tab_widget.addTab(tab, f"{i}")

        
        main_layout.addWidget(tab_widget)

        self.setLayout(main_layout)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
