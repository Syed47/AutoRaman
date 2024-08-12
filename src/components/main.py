from PyQt5.QtWidgets import QApplication, QWidget, QHBoxLayout, QTabWidget

from components.log_console import LogConsole
from components.settings_tab import SettingsTab
from components.autofocus_tab import AutofocusTab
from components.laser_tab import LaserTab
# from components.cells_tab import CellsTab
# from components.spectra_tab import SpectraTab
# from components.repeat_tab import RepeatTab
# from components.optimise_tab import OptimiseTab
from components.style import StyleSheet  

import sys



class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.state = {}
        self.init_ui()
        

    def init_ui(self):
        self.setWindowTitle("AutoRaman")
        self.setGeometry(100, 100, 870, 660)

        main_layout = QHBoxLayout(self)

        tab_widget = QTabWidget()
        tab_widget.setStyleSheet(StyleSheet)
        tab_widget.setFixedSize(800, 640)
        
        self.logger = LogConsole(self)

        self.settings_tab = SettingsTab(self.logger)
        tab_widget.addTab(self.settings_tab, 'Settings')

        self.autofocus_tab = AutofocusTab(self.logger)
        tab_widget.addTab(self.autofocus_tab, 'Autofocus')

        self.laser_tab = LaserTab(self.logger)
        tab_widget.addTab(self.laser_tab, 'Laser')

        # self.cells_tab = CellsTab(self.logger)
        # tab_widget.addTab(self.cells_tab, 'Cells')

        # self.spectra_tab = SpectraTab(self.logger)
        # tab_widget.addTab(self.spectra_tab, 'Spectra')

        # self.repeat_tab = RepeatTab(self.logger)
        # tab_widget.addTab(self.repeat_tab, 'Repeat')

        # self.optimise_tab = OptimiseTab(self.logger)
        # tab_widget.addTab(self.optimise_tab, 'Optimise')

        main_layout.addWidget(tab_widget)
        main_layout.addWidget(self.logger)

        self.setLayout(main_layout)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyleSheet(StyleSheet)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
