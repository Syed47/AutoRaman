
from pycromanager import Core, start_headless, stop_headless
from Microscope import Microscope
from Autofocus import Autofocus, Raman


# Test Script
ms:Microscope = Microscope()
raman:Autofocus = Raman(ms.lamp, ms.camera, ms.stage)
ms.set_auto_focus(strategy=raman)
ms.set_exposure(16)
ms.perform_auto_focus()
