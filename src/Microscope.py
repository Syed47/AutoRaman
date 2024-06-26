from pycromanager import Core, start_headless, stop_headless
from Lamp import Lamp
from Stage import Stage
from Camera import Camera

class Microscope:
    def __init__(self, headless=True, core_app_path="C:\\Program Files\\Micro-Manager-2.0", config_file="IX81_LUDL_amscope_Laser532.cfg"):
        self.core_app_path = core_app_path
        self.config_file = f"{self.core_app_path}\\{config_file}"
        self.headless = headless
        
        self._initialize_core()

        self.lamp = Lamp(self.core)
        self.stage = Stage(self.core)
        self.camera = Camera(self.core)

    def _initialize_core(self):
        if self.headless:
            start_headless(self.core_app_path, self.config_file, debug=False)
        self.core = Core()
        self.core.load_system_configuration(self.config_file)


    def auto_focus(self, strategy:Autofocus, start, end, step=1):
        self.focus_strategy = strategy(self)
        self.focus_strategy.zscan(start, end, step)
        return self.focus_strategy.focus()

    def __del__(self):
        if self.headless:
            stop_headless()

