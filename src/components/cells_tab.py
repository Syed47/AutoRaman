from PyQt5.QtWidgets import  QVBoxLayout, QLabel

from tab import Tab

class CellsTab(Tab):
    def __init__(self, logger=None):
        super().__init__(logger)
        self.init_ui()
        self.connect_signals()

    def init_ui(self):        
        tab_layout = QVBoxLayout()
        tab_layout.addWidget(QLabel("This is Cells"))
        self.setLayout(tab_layout)

    def connect_signals(self):
        pass

