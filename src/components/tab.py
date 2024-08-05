from PyQt5.QtWidgets import QWidget
from abc import ABC, ABCMeta, abstractmethod
from components.style import StyleSheet

class QWidgetABCMeta(type(QWidget), ABCMeta):
    pass

class Tab(QWidget, ABC, metaclass=QWidgetABCMeta):

    def __init__(self, logger=None):
        super().__init__()
        self.logger = logger
        self.setStyleSheet(StyleSheet)

    @abstractmethod
    def init_ui(self):
        pass

    @abstractmethod
    def connect_signals(self):
        pass

    # @abstractmethod
    # def preprocess(self):
    #     pass

    # @abstractmethod
    # def postprocess(self):
    #     pass



