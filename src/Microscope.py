
from pycromanager import Core, start_headless, stop_headless
from Lamp import Lamp
from Stage import Stage
from Camera import Camera
from Autofocus import Autofocus, Raman


class Microscope:
    def __init__(self, headless=True, config_file:str="IX81_LUDL_amscope_Laser532.cfg"):
        self.core_app_path = "C:\\Program Files\\Micro-Manager-2.0"
        self.config_file = f"{self.core_app_path}\\{config_file}"
        if headless:
            start_headless(self.core_app_path, config_file, debug=False)
        self.core = Core()            
        self.core.load_system_configuration(config_file)

        self.lamp = Lamp(self.core)
        self.stage = Stage(self.core)
        self.camera = Camera(self.core)
        self.auto_focus = Autofocus(lamp=self.lamp, camera=self.camera, stage=self.stage)

    def move_stage(self, x, y, z):
        self.stage.move(x, y, z)
    
    def capture_image(self, invert=False, path="Capture"):
        return self.camera.snap_image()

    def capture_spectra(self):
        pass

    def turn_lamp(self, on=False):
        if on:
            self.lamp.set_on()
        else:
            self.lamp.set_off()
    
    def set_exposure(self, val=15):
        self.core.set_exposure(val)

    def set_auto_focus(self, strategy=Autofocus):
        self.auto_focus = strategy

    def perform_auto_focus(self):
        return self.auto_focus.focus()



