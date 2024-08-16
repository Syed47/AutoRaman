from PyQt5.QtWidgets import QWidget
from PyQt5.QtCore import QTimer
from abc import ABC, ABCMeta, abstractmethod
from components.style import StyleSheet

class QWidgetABCMeta(type(QWidget), ABCMeta):
    pass

class Tab(QWidget, ABC, metaclass=QWidgetABCMeta):

    __state = {}

    def __init__(self, logger=None):
        super().__init__()
        self.logger = logger
        self.setStyleSheet(StyleSheet)
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update)
        self.timer.start(500)

    @abstractmethod
    def update(self):
        pass

    @abstractmethod
    def preprocess(self):
        pass

    @abstractmethod
    def postprocess(self):
        pass

    @abstractmethod
    def init_ui(self):
        pass

    @abstractmethod
    def connect_signals(self):
        pass

