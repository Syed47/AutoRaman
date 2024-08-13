from core.controller import controller
from core.microscope import microscope

class StateManager:
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(StateManager, cls).__new__(cls)
        return cls._instance

    def __init__(self):
        if not hasattr(self, '_initialized'):
            self._state = {}
            self._initialized = True
    
    def set(self, key, value):
        if value is None:
            print(f"Invalid input for key {key}: {value}")
            return

        actions = {
            "LAMP": lambda val: microscope.lamp.set_on() if val else microscope.lamp.set_off(),
            "LASER": lambda val: controller.set_serial_port_command("COM4", f"CURRENT={val}", "\r\n") if val >= 0 else None,
            "LAMP-VOLTAGE": lambda val: controller.set_property("TransmittedLamp", "Voltage", val) if 0 <= val <= 12 else None,
            "EXPOSURE": lambda val: microscope.camera.set_exposure(val),
            "AUTO-EXPOSURE": lambda val: microscope.camera.set_option("ExposureAuto", "1" if val else "0"),
            "BINNING": lambda val: microscope.camera.set_option("Binning", val if val in ['1x1', '2x2', '4x4'] else '1x1'),
            "PIXEL-TYPE": lambda val: microscope.camera.set_option("PixelType", val if val in ['GREY8', 'RGB32'] else 'GREY8'),
            "FILTER-POSITION": lambda val: controller.set_property("FilterCube", "Label", val) if val[::-1] and 0 < int(val[:-1]) < 7 else None
        }

        action = actions.get(key)
        if action:
            action(value)
            self._state[key] = value
        else:
            print(f"Key {key} is not recognized")
        
        return value

    def get(self, key):
        return self._state.get(key)


state_manager = StateManager()

state_manager.set("LAMP", False)
state_manager.set("LASER", 0)
state_manager.set("LAMP-VOLTAGE", 11)
state_manager.set("EXPOSURE", 15)
state_manager.set("AUTO-EXPOSURE", True)
state_manager.set("BINNING", '1x1')
state_manager.set("PIXEL-TYPE", 'GREY8')
state_manager.set("FILTER-POSITION", 'Position-1')

__all__ = ['state_manager']
