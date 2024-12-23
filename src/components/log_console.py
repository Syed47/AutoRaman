from PyQt5.QtWidgets import QWidget, QVBoxLayout, QTextEdit, QPushButton
from PyQt5.QtCore import Qt

class LogConsole(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.init_ui()

    def init_ui(self):
        self.log_layout = QVBoxLayout(self)

        self.log_console = QTextEdit()
        self.log_console.setReadOnly(True)
        self.log_console.hide()

        self.collapse_button = QPushButton(">>")
        self.collapse_button.setFixedSize(26, 32)
        self.collapse_button.setCheckable(True)
        self.collapse_button.toggled.connect(self.toggle_log_console)
        self.collapse_button.setStyleSheet("""
            QPushButton {
                font-size: 12px; /* Smaller font size */
                background: #444444; /* Dark background */
                color: white; /* White text */
                border: none; /* Remove border */
                border-radius: 4px; /* Rounded corners */
                padding: 5px; /* Padding around the text */
            }
            QPushButton:checked {
                background: #555555; /* Slightly lighter background when checked */
            }
            QPushButton:hover {
                background: #555555; /* Lighter background on hover */
            }
        """)

        self.log_layout.addWidget(self.collapse_button, alignment=Qt.AlignCenter)
        self.log_layout.addWidget(self.log_console)

    def toggle_log_console(self, checked):
        if checked:
            self.log_console.show()
            self.collapse_button.setText("<<")
            self.parentWidget().setFixedSize(1040, 660)
        else:
            self.log_console.hide()
            self.collapse_button.setText(">>")
            self.parentWidget().setFixedSize(870, 660)

    def log(self, message):
        self.log_console.append(message)
