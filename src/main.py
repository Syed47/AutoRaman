import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QFrame, QLabel, QPushButton, QLineEdit, QRadioButton, QSizePolicy, QTabWidget, QFormLayout, QFrame
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("AutoRaman")
        self.setGeometry(100, 100, 800, 600)

        # Main layout
        main_layout = QHBoxLayout()

        # Create the QTabWidget
        tab_widget = QTabWidget()
        tab_widget.setStyleSheet("""
            QTabBar::tab {
                height: 24px;
                width: 160px;
                font-size: 12pt;
            }
        """)

        # Create Tab 1
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
        """)

        # Create the QFrame for Tab 1
        frame_tab1 = QFrame()
        frame_tab1.setFrameShape(QFrame.StyledPanel)
        frame_tab1_layout = QHBoxLayout()

        # Left panel in frame_tab1 with input fields, radio buttons, and finish button
        left_panel = QFrame()
        left_panel.setFrameShape(QFrame.StyledPanel)
        left_layout = QFormLayout()

        line_edit1 = QLineEdit()
        line_edit1.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        line_edit2 = QLineEdit()
        line_edit2.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        line_edit3 = QLineEdit()
        line_edit3.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)

        left_layout.addRow("Start (mm):", line_edit1)
        left_layout.addRow("End (mm):", line_edit2)
        left_layout.addRow("Step (mm):", line_edit3)

        # Add horizontal line separator
        line_separator = QFrame()
        line_separator.setFrameShape(QFrame.HLine)
        line_separator.setFrameShadow(QFrame.Sunken)
        left_layout.addRow(line_separator)

        radio_button1 = QRadioButton("Amplitude")
        radio_button2 = QRadioButton("Phase")
        radio_button1.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        radio_button2.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        radio_layout = QVBoxLayout()
        radio_layout.addWidget(radio_button1)
        radio_layout.addWidget(radio_button2)


        # Center align radio buttons vertically and horizontally
        radio_layout.setAlignment(Qt.AlignCenter)
        left_layout.addRow("Autofocus Strategy:", radio_layout)

        # Add horizontal line separator
        line_separator = QFrame()
        line_separator.setFrameShape(QFrame.HLine)
        line_separator.setFrameShadow(QFrame.Sunken)
        left_layout.addRow(line_separator)

        run_button = QPushButton("Run")
        run_button.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        left_layout.addWidget(run_button)

        # Set alignment and spacing for the left panel layout
        left_layout.setLabelAlignment(Qt.AlignCenter)
        left_layout.setHorizontalSpacing(20)  # Example spacing between labels and widgets
        left_layout.setVerticalSpacing(20)
        left_layout.setFieldGrowthPolicy(QFormLayout.AllNonFixedFieldsGrow)
        left_panel.setLayout(left_layout)

        # Right panel in frame_tab1 with image view
        right_panel = QFrame()
        right_panel.setFrameShape(QFrame.StyledPanel)
        right_layout = QVBoxLayout()

        # Default image to show
        pixmap1 = QPixmap("../Autofocus/image_19.tif")
        image_label1 = QLabel()
        image_label1.setPixmap(pixmap1)
        image_label1.setFixedSize(400, 300)  # Set fixed size for the image label
        image_label1.setScaledContents(True)  # Maintain aspect ratio and scale contents
        right_layout.addWidget(image_label1)

        # Add horizontal line separator
        line_separator2 = QFrame()
        line_separator2.setFrameShape(QFrame.HLine)
        line_separator2.setFrameShadow(QFrame.Sunken)
        right_layout.addWidget(line_separator2)

        pixmap2 = QPixmap("../Autofocus/image_1.tif")
        image_label2 = QLabel()
        image_label2.setPixmap(pixmap2)
        image_label2.setFixedSize(400, 300)  # Set fixed size for the image label
        image_label2.setScaledContents(True)  # Maintain aspect ratio and scale contents
        right_layout.addWidget(image_label2)

        # Add horizontal line separator
        line_separator2 = QFrame()
        line_separator2.setFrameShape(QFrame.HLine)
        line_separator2.setFrameShadow(QFrame.Sunken)
        right_layout.addWidget(line_separator2)

        zfocus = QLineEdit()
        zfocus.setPlaceholderText("Z-Focus (mm)")
        zfocus.setReadOnly(True)
        zfocus.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        right_layout.addWidget(zfocus)

        right_panel.setLayout(right_layout)

        # Add left and right panels to frame_tab1 layout with proportional width
        frame_tab1_layout.addWidget(left_panel, 2)  # Left panel takes 2/3 of the space
        frame_tab1_layout.addWidget(right_panel, 1)  # Right panel takes 1/3 of the space
        frame_tab1.setLayout(frame_tab1_layout)

        # Add frame_tab1 to tab1 layout
        tab1_layout.addWidget(frame_tab1)
        tab1.setLayout(tab1_layout)

        # Add tab1 to the QTabWidget
        tab_widget.addTab(tab1, "Autofocus")

        # Add additional tabs
        for i in ['Laser', 'Cells', 'Spectra', 'Repeat', 'Optimise']:
            tab = QWidget()
            tab_layout = QVBoxLayout()
            tab_layout.addWidget(QLabel(f"This is Tab {i}"))
            tab.setLayout(tab_layout)
            tab_widget.addTab(tab, f"{i}")

        # Add QTabWidget to the main layout
        main_layout.addWidget(tab_widget)

        self.setLayout(main_layout)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
