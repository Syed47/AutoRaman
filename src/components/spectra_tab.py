from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel

class SpectraTab(QWidget):
    def __init__(self, logger=None):
        super().__init__()
        self.logger = logger
        self.initUI()

    def initUI(self):
        tab_layout = QVBoxLayout()
        tab_layout.addWidget(QLabel("This is Spectra"))
        self.setLayout(tab_layout)

    def get_widget(self):
        return self
