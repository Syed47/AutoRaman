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
            "FILTER-POSITION": lambda val: controller.set_property("FilterCube", "Label", val),
            "INVERTED-IMAGE": lambda val : None,
            "ZFOCUS": lambda val: None,
            "LASER-FOCUS": lambda val: None,
            "LASER-OFFSET": lambda val: None,
            "ZSTART": lambda val: None,
            "ZEND": lambda val: None,
            "ZSTEP": lambda val: None
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

state_manager.set('LAMP', False)
state_manager.set('LASER', 0)
state_manager.set('BINNING', '1x1')
state_manager.set('PIXEL-TYPE', 'GREY8')
state_manager.set('FILTER-POSITION', controller.get_property("FilterCube", "Label"))
state_manager.set('EXPOSURE', 15)
state_manager.set('AUTO-EXPOSURE', False)
state_manager.set('LAMP-VOLTAGE', 10)
state_manager.set('INVERTED-IMAGE', False)
state_manager.set('ZSTART', microscope.stage.z - 10)
state_manager.set('ZEND', microscope.stage.z + 10)
state_manager.set('ZSTEP', 1)

__all__ = ['state_manager']
