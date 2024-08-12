from PyQt5.QtWidgets import QWidget
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

    @classmethod
    def get_state(cls, key):
        return cls.__state.get(key)

    @classmethod
    def set_state(cls, key, value):

        # if key == "LAMP":
        #     pass
        # elif key == "LASER":
        #     pass
        # elif key == "LAMP-VOLTAGE":
        #     pass
        # elif key == "LASER-CURRENT":
        #     pass
        # elif key == "EXPOSURE":
        #     pass
        # elif key == "INVERTED-IMAGE":
        #     pass
        # elif key == "AUTO-EXPOSURE":
        #     pass
        # elif key == "BINNING":
        #     pass
        # elif key == "PIXEL-TYPE":
        #     pass
        # elif key == "FILTER-POSITION":
        #     pass
        # elif key == "LASER-OFFSET":
        #     pass
        cls.__state[key] = value
        print(cls.__state)


    @classmethod
    def reset_state(cls):
        cls.__state.clear()

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
