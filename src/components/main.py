import sys
from PyQt5.QtWidgets import QApplication, QWidget, QHBoxLayout, QTabWidget

from log_console import LogConsole
from settings_tab import SettingsTab
from autofocus_tab import AutofocusTab
from laser_tab import LaserTab
from cells_tab import CellsTab
from spectra_tab import SpectraTab
from repeat_tab import RepeatTab
from optimise_tab import OptimiseTab
from style import style_sheet  

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("AutoRaman")
        self.setGeometry(100, 100, 870, 660)

        main_layout = QHBoxLayout(self)

        tab_widget = QTabWidget()
        tab_widget.setStyleSheet(style_sheet)
        tab_widget.setFixedSize(800, 640)
        
        self.logger = LogConsole(self)

        self.settings_tab = SettingsTab(self.logger)
        tab_widget.addTab(self.settings_tab.get_widget(), 'Settings')

        self.autofocus_tab = AutofocusTab(self.logger)
        tab_widget.addTab(self.autofocus_tab.get_widget(), 'Autofocus')

        self.laser_tab = LaserTab(self.logger)
        tab_widget.addTab(self.laser_tab.get_widget(), 'Laser')

        self.cells_tab = CellsTab(self.logger)
        tab_widget.addTab(self.cells_tab.get_widget(), 'Cells')

        self.spectra_tab = SpectraTab(self.logger)
        tab_widget.addTab(self.spectra_tab.get_widget(), 'Spectra')

        self.repeat_tab = RepeatTab(self.logger)
        tab_widget.addTab(self.repeat_tab.get_widget(), 'Repeat')

        self.optimise_tab = OptimiseTab(self.logger)
        tab_widget.addTab(self.optimise_tab.get_widget(), 'Optimise')

        main_layout.addWidget(tab_widget)
        main_layout.addWidget(self.logger.get_widget())

        self.setLayout(main_layout)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyleSheet(style_sheet)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
