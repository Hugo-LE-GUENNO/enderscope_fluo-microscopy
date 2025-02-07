from EnderPiLightCore import EnderPiLightCore
from EnderPiLightUI import EnderPiLightUI
import board
import neopixel


class EnderPiLight:
    def __init__(self, total_pixels=1, board_pin=board.D18, start_pin=0, end_pin=None, use_ui=True, title="EnderPiLight"):
        if use_ui:
            self.light = EnderPiLightUI(total_pixels, board_pin, start_pin, end_pin, title)
        else:
            self.light = EnderPiLightCore(total_pixels, board_pin, start_pin, end_pin)

    def get_controls(self):
        """Return the UI controls if available."""
        if hasattr(self.light, 'get_controls'):
            return self.light.get_controls()
        return None

    def get_title(self):
        """Return the title for the tab."""
        if hasattr(self.light, 'get_title'):
            return self.light.get_title()
        return self.__class__.__name__