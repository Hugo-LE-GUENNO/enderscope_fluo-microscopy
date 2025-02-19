import ipywidgets as widgets
from EnderPiLightCore import EnderPiLightCore
import board

class EnderPiLightUI:
    def __init__(self, total_pixels=1, board_pin=board.D18, start_pin=0, end_pin=None, title="EnderPiLight"):
        # Initialize the core functionality
        self.core = EnderPiLightCore(total_pixels, board_pin, start_pin, end_pin)
        self.title = title

        # Create UI elements
        self.toggle_button = widgets.Button(description="Toggle Light", style={'button_color': '#cccccc'})  # Gray color
        self.toggle_button.on_click(self.on_toggle_click)

        # Create a color indicator (Gray for OFF, Bright Green for ON)
        self.state_indicator = widgets.Button(description="", layout=widgets.Layout(width='20px', height='20px', border='solid 1px #cccccc'))
        self.update_state_indicator()

        # Create RGB sliders
        self.red_slider = widgets.IntSlider(
            value=255,  # Initial Red value
            min=0, 
            max=255, 
            description='Red:',
            continuous_update=True
        )
        self.green_slider = widgets.IntSlider(
            value=255,  # Initial Green value
            min=0, 
            max=255, 
            description='Green:',
            continuous_update=True
        )
        self.blue_slider = widgets.IntSlider(
            value=255,  # Initial Blue value
            min=0, 
            max=255, 
            description='Blue:',
            continuous_update=True
        )
        self.red_slider.observe(self.on_color_change, names='value')
        self.green_slider.observe(self.on_color_change, names='value')
        self.blue_slider.observe(self.on_color_change, names='value')

        # Create intensity slider
        self.intensity_slider = widgets.FloatSlider(
            value=1.0,  # Initial intensity
            min=0.0, 
            max=1.0, 
            step=0.01, 
            description='Intensity:',
            continuous_update=True
        )
        self.intensity_slider.observe(self.on_intensity_change, names='value')

        # Create a color preview box using HTML
        self.color_preview = widgets.HTML(
            value='<div style="width: 100px; height: 100px; border: solid 1px #cccccc;"></div>',
            layout=widgets.Layout(border='solid 1px #cccccc')
        )
        self.update_color_preview()

        # Organize the button, indicator, sliders, and color preview into a vertical layout
        self.ui_layout = widgets.VBox([
            self.toggle_button, 
            self.state_indicator, 
            self.intensity_slider, 
            self.red_slider, 
            self.green_slider, 
            self.blue_slider, 
            self.color_preview
        ])

    def update_state_indicator(self):
        """Update the color of the state indicator based on light status."""
        color = '#00FF00' if self.core.is_on else '#E8E8E8'
        self.state_indicator.style.button_color = color

    def on_intensity_change(self, change):
        """Handle intensity slider changes."""
        self.core.set_intensity(change['new'])  # Update intensity in core

    def on_color_change(self, change):
        """Handle RGB slider changes and update the color preview."""
        r = self.red_slider.value
        g = self.green_slider.value
        b = self.blue_slider.value
        self.core.set_rgb_color(r, g, b)  # Update RGB color in core
        self.update_color_preview()  # Update preview color

    def update_color_preview(self):
        """Update the color preview box based on RGB values."""
        r = self.red_slider.value
        g = self.green_slider.value
        b = self.blue_slider.value
        color_hex = self._rgb_to_hex(r, g, b)
        self.color_preview.value = f'<div style="width: 100px; height: 100px; background-color: {color_hex}; border: solid 1px #cccccc;"></div>'

    def _rgb_to_hex(self, r, g, b):
        """Convert RGB values to HEX color."""
        return f'#{r:02X}{g:02X}{b:02X}'

    def on_toggle_click(self, b):
        """Handle toggle button click and update the state indicator."""
        self.core.toggle()
        self.update_state_indicator()  # Update the indicator color

    def get_title(self):
        """Return the title of the UI."""
        return self.title

    def get_controls(self):
        """Return the UI controls with the toggle button and state indicator."""
        return self.ui_layout

    def get_output(self):
        """No output for this UI component, return None."""
        return None
