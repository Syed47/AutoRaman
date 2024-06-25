# Test Script

from Microscope import Microscope
from Autofocus import BrightSpot

ms = Microscope()

ms.camera.set_option("Binning", "1x1")
ms.camera.set_option("PixelType", "GREY8")
ms.camera.set_option("ExposureAuto", "0")
ms.camera.set_exposure(16)

result = ms.auto_focus(strategy_class=BrightSpot, start=1350, end=1400)
print(result)
