from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel

from tab import Tab

class RepeatTab(Tab):
    def __init__(self, logger=None):
        super().__init__(logger)
        self.init_ui()

    def init_ui(self):
        tab_layout = QVBoxLayout()
        tab_layout.addWidget(QLabel("This is Repeat"))
        self.setLayout(tab_layout)
    
    def connect_signals(self):
        pass
