import io
from PIL import Image as PILImage, ImageFilter
from picamera2 import Picamera2
#from EnderPiAutofocus import EnderPiAutofocusCore
import numpy as np
import time
import scipy.ndimage

class EnderPiCamCore:
    def __init__(self, resolution=(2028,1520), exposure=500000, gain=1.0, autofocus=False, stage=None):
        self.picam2 = Picamera2()
        self.resolution = resolution
        self.exposure = exposure
        self.gain = gain
        self.autofocus_enabled = autofocus
        self.stage = stage  # Optional stage for autofocus
        self.scores = []

        # Configure the camera
        self._config = self.picam2.create_still_configuration({'format': 'RGB888', 'size': self.resolution})
        self.picam2.configure(self._config)
        self.set_controls(exposure=self.exposure, gain=self.gain)
        self.picam2.start()

    def set_controls(self, exposure=None, gain=None):
        controls = {}
        if exposure is not None:
            self.exposure = exposure
            controls['ExposureTime'] = self.exposure
        if gain is not None:
            self.gain = gain
            controls['AnalogueGain'] = self.gain
        self.picam2.set_controls(controls)

    def capture(self, path=None, green=False):
        """Capture a still image. If a path is provided, save the image to the specified path, else return it as a PIL image."""
        buffer = io.BytesIO()
        
        # Capture the image to a buffer
        self.picam2.capture_file(buffer, format='png')
        buffer.seek(0)

        # Open the image from the buffer
        image = PILImage.open(buffer)
        
        if green:
            # Extract only the green channel and return it as a grayscale image
            _, green_channel, _ = image.split()
            image = green_channel
        
        if path:
            # Save the image to the specified path
            image.save(path, 'PNG')
            print(f"Image saved to {path}")
        else:
            # Return the image as a PIL image
            return image

    def autofocus(self):
        def calculate_focus_score():
            """Calculate focus score using edge enhancement and variance."""
            image = self.capture()
            _, image, _ = image.split()
            #edges_image = image.filter(ImageFilter.GaussianBlur(radius=2))
            #edges_image = image.filter(ImageFilter.EDGE_ENHANCE_MORE)
            image = np.array(image)

            laplacian_kernel = np.array([[0, 1, 0],
                                 [1, -4, 1],
                                 [0, 1, 0]])
            laplacian = np.abs(scipy.ndimage.convolve(image, laplacian_kernel))
            variance = laplacian.var()
            
            return variance
    
        # Coarse search
        step_initial = 0.05
        nSlices = 10
        offset_topPosition = (nSlices * step_initial) / 2
        self.stage.move_relative(0, 0, offset_topPosition + step_initial)
        
        focus_data = []
        for _ in range(nSlices):
            self.stage.move_relative(0, 0, -step_initial)
            current_pos = self.stage.get_position()
            focus_score = calculate_focus_score()
            focus_data.append((current_pos, focus_score))
        
        # Find the best position from the coarse search
        best_focus_position, best_focus_score = min(focus_data, key=lambda x: x[1])
        self.stage.move_absolute(best_focus_position[0], best_focus_position[1], best_focus_position[2])
    
        #Fine search
        step_fine = 0.04
        max_steps = 20
        
        # Fine search upwards
        for i in range(max_steps):
            self.stage.move_relative(0, 0, step_fine)  # Move upwards
            current_pos = self.stage.get_position()
            focus_score = calculate_focus_score()
            
            if focus_score < best_focus_score:
                best_focus_score = focus_score
                best_focus_position = current_pos
            else:
                print(f"Focus decreased upwards, stopping at step {i}.")
                break
    
        self.stage.move_absolute(best_focus_position[0], best_focus_position[1], best_focus_position[2])
    
        # Fine search downwards
        for i in range(max_steps):
            self.stage.move_relative(0, 0, -step_fine)  # Move downwards
            current_pos = self.stage.get_position()
            focus_score = calculate_focus_score()
            
            if focus_score < best_focus_score:
                best_focus_score = focus_score
                best_focus_position = current_pos
            else:
                print(f"Focus decreased downwards, stopping at step {i}.")
                break
    
        # Move stage to the best focus position found
        self.stage.move_absolute(best_focus_position[0], best_focus_position[1], best_focus_position[2])
    
        return best_focus_position #best_focus_position