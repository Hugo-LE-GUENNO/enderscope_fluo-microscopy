import io
import time
import threading
import ipywidgets as widgets
import numpy as np
from PIL import Image
from EnderPiCamCore import EnderPiCamCore

class EnderPiCamUI:
    def __init__(self, resolution=(2028,1520), exposure=10000, gain=4.0, title="EnderPiCam", ui=True, autofocus=False, stage = None):
        self.core = EnderPiCamCore(resolution, exposure, gain, stage, autofocus)
        self.title = title
        self.ui = ui
        self.preview_running = False
        self.autofocus_enabled = autofocus
        
        # Create autofocus button
        self.autofocus_button = widgets.Button(description="Autofocus", icon='camera')
        self.autofocus_button.on_click(self.run_autofocus)
        
        # Initialize UI elements
        self.preview_image = widgets.Image(format='jpeg', width=resolution[0], height=resolution[1])

        # Exposure slider
        self.exposure_slider = widgets.IntSlider(
            value=self.core.exposure,
            min=1,
            max=1000000,
            step=100,
            description='Exposure Time',
            continuous_update=True
        )
        self.exposure_slider.observe(self.update_exposure, names='value')

        # Gain slider
        self.gain_slider = widgets.FloatSlider(
            value=self.core.gain,
            min=1.0,
            max=10.0,
            step=0.1,
            description='Gain',
            continuous_update=True
        )
        self.gain_slider.observe(self.update_gain, names='value')

        # Capture button
        self.capture_button = widgets.Button(description="Capture Image")
        self.capture_button.on_click(self.capture_image)

        # Status indicator
        self.status_indicator = widgets.HTML(
            value=self._get_status_indicator_html('gray'),
            layout=widgets.Layout(width='30px', height='30px')
        )

        # File picker
        self.file_picker = widgets.Text(
            description="Save As:",
            placeholder="Enter file path",
            value="image.jpg"
        )

        # Preview toggle button
        self.preview_button = widgets.Button(description="Toggle Preview")
        self.preview_button.on_click(self.toggle_preview)

        self.output = widgets.Textarea(
            value='Hello World',
            placeholder='Type something',
            description='',
            disabled=True  
        )

        if self.ui:
            self.ui_layout = widgets.VBox([
                widgets.HBox([self.preview_button, self.status_indicator]),
                self.exposure_slider,
                self.gain_slider,
                self.file_picker,
                self.capture_button,
                self.autofocus_button,  # Add autofocus button to the layout
                self.output
            ])
            
    def _get_status_indicator_html(self, color):
        """Generate HTML for the status indicator."""
        return f'<div style="border-radius: 50%; width: 20px; height: 20px; background-color: {color};"></div>'

    def update_exposure(self, change):
        self.core.set_controls(exposure=change['new'])

    def update_gain(self, change):
        self.core.set_controls(gain=change['new'])

    def capture_image(self, b):
        image = self.core.capture()
        file_path = self.file_picker.value
        if file_path:
            image.save(file_path)
            self.output.value = f"Image saved as {file_path}"

    def toggle_preview(self, b):
        if self.preview_running:
            self.stop_preview()
        else:
            self.start_preview()

    def start_preview(self):
        """Start preview in a separate thread."""
        self.preview_running = True
        self.status_indicator.value = self._get_status_indicator_html('#00FF00')
        threading.Thread(target=self._preview_loop).start()

    def stop_preview(self):
        """Stop preview."""
        self.status_indicator.value = self._get_status_indicator_html('gray')
        self.preview_running = False

    def _preview_loop(self):
        while self.preview_running:
            imageRaw = self.core.capture()
            image_gray = imageRaw.convert('L')
            image_array = np.array(image_gray)
            min_val = np.min(image_array)
            max_val = np.max(image_array)
            normalized_image = (image_array - min_val) * (255.0 / (max_val - min_val))
            image = Image.fromarray(np.uint8(normalized_image))
            with io.BytesIO() as output:
                image.save(output, format="JPEG")
                self.preview_image.value = output.getvalue()
            time.sleep(0.1)

    def run_autofocus(self, b):
        self.output.value = "running..."
        best_focus_position = self.core.autofocus()  # Call the autofocus method
        formatted_position = f"Best focus position: {best_focus_position}"
        self.output.value = formatted_position  # Update output with the result


    def get_controls(self):
        if self.ui:
            return self.ui_layout
        return None

    def get_output(self):
        return self.preview_image if self.ui else None

    def get_title(self):
        return self.title
