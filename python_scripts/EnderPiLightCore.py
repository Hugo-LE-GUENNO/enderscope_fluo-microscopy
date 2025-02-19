import neopixel
import board
import threading
import time


class EnderPiLightCore:
    # Global buffer to hold the state of all pixels across all lights
    global_pixel_state = []
    global_pixel_count = 0

    def __init__(self, total_pixels=1, board_pin=board.D18, start_pin=0, end_pin=None):
        self.total_pixels = total_pixels
        self.start_pin = start_pin
        self.end_pin = end_pin if end_pin is not None else total_pixels

        # Initialize or expand global_pixel_state if needed
        if EnderPiLightCore.global_pixel_count < total_pixels:
            # Expand global state if necessary
            EnderPiLightCore.global_pixel_state = [(0, 0, 0)] * total_pixels
            EnderPiLightCore.global_pixel_count = total_pixels

        # Initialize NeoPixel object
        self.pixels = neopixel.NeoPixel(board_pin, total_pixels, auto_write=False)

        self.is_on = False  # Light starts off by default
        self.rgb_color = (255, 255, 255)  # Default color is white
        self.intensity = 1.0  # Default intensity

    def update_pixels(self):
        """Update the physical NeoPixel strip with the global state."""
        for i in range(self.total_pixels):
            self.pixels[i] = EnderPiLightCore.global_pixel_state[i]
        self.pixels.show()

    def toggle(self):
        """Toggle the light on and off for the assigned pixel range."""
        self.is_on = not self.is_on
        if self.is_on:
            # Turn on the light only within the assigned pixel range
            for i in range(self.start_pin, self.end_pin):
                if i < EnderPiLightCore.global_pixel_count:  # Ensure within bounds
                    EnderPiLightCore.global_pixel_state[i] = self._apply_intensity(self.rgb_color)
            print(f"Light ON from pixel {self.start_pin} to {self.end_pin - 1}")
        else:
            # Turn off the light only within the assigned pixel range
            for i in range(self.start_pin, self.end_pin):
                if i < EnderPiLightCore.global_pixel_count:  # Ensure within bounds
                    EnderPiLightCore.global_pixel_state[i] = (0, 0, 0)
            print(f"Light OFF from pixel {self.start_pin} to {self.end_pin - 1}")

        # Update the NeoPixel strip with the new global state
        self.update_pixels()

    def set_intensity(self, value):
        """Set the light intensity."""
        self.intensity = value
        if self.is_on:
            # Update the color with the new intensity
            for i in range(self.start_pin, self.end_pin):
                if i < EnderPiLightCore.global_pixel_count:  # Ensure within bounds
                    EnderPiLightCore.global_pixel_state[i] = self._apply_intensity(self.rgb_color)
            # Refresh the display
            self.update_pixels()

    def _apply_intensity(self, color):
        """Apply intensity to the color."""
        r, g, b = color
        r = int(r * self.intensity)
        g = int(g * self.intensity)
        b = int(b * self.intensity)
        # Ensure values are within the 0-255 range
        r = min(max(r, 0), 255)
        g = min(max(g, 0), 255)
        b = min(max(b, 0), 255)
        return (r, g, b)

    def set_rgb_color(self, r, g, b):
        """Set the RGB color of the light."""
        self.rgb_color = (r, g, b)
        if self.is_on:
            # Update the color with the new RGB values
            for i in range(self.start_pin, self.end_pin):
                if i < EnderPiLightCore.global_pixel_count:  # Ensure within bounds
                    EnderPiLightCore.global_pixel_state[i] = self._apply_intensity(self.rgb_color)
            # Refresh the display
            self.update_pixels()