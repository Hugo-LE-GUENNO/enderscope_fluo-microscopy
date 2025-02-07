from EnderPiCamCore import EnderPiCamCore
from EnderPiCamUI import EnderPiCamUI
#from EnderPiAutofocus import EnderPiAutofocusCore  # Assuming autofocus is implemented separately

class EnderPiCam(EnderPiCamUI):
    def __init__(self, resolution=(256,256), exposure=10000, gain=4.0, title="EnderPiCam", ui=True, autofocus=False, stage=None):
        super().__init__(resolution, exposure, gain, title, ui, stage, autofocus)
        
