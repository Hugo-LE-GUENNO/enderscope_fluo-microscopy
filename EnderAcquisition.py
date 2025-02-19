from EnderAcquisitionCore import EnderAcquisitionCore
from EnderAcquisitionUI import EnderAcquisitionUI

class EnderAcquisition:
    def __init__(self, use_ui=True, title="EnderAcquisition", stage=None, camera=None, lightBF=None, lightFluo=None):
        self.stage = stage
        self.camera = camera
        self.title = title
        self.path =""
        self.lightBF=lightBF
        self.lightFluo=lightFluo
        
        if use_ui:
            self.acquisition = EnderAcquisitionUI(title=title, stage = stage, camera=camera, lightFluo=lightFluo, lightBF=lightBF)
        else:
            self.acquisition = EnderAcquisitionCore(title=title, stage = stage, camera=camera, lightFluo=lightFluo, lightBF=lightBF)

    def get_controls(self):
        if hasattr(self.acquisition, 'get_controls'):
            return self.acquisition.get_controls()
        return None

    def get_output(self):
        if hasattr(self.acquisition, 'get_output'):
            return self.acquisition.get_output()
        return None

    def get_title(self):
        if hasattr(self.acquisition, 'get_title'):
            return self.acquisition.title
        return self.__class__.__name__
