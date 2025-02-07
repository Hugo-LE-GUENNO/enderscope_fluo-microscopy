class EnderAcquisitionCore:
    def __init__(self, stage, camera):
        self.positions = []
        self.timelapse_settings = {"frame": 0, "interval": 0}
        self.mosaic_settings = {"rows": 0, "columns": 0}
        self.stage = stage
        self.camera = camera

    
    def save_position(self, position):
        """Save a position."""
        self.positions.append(position, self.stage.get_position())
    
    def delete_position(self, position):
        """Delete a specific position."""
        if position in self.positions:
            self.positions.remove(position)
    
    def reset_positions(self):
        """Reset all positions."""
        self.positions.clear()
    
    def go_to_position(self, position):
        """Simulate going to a position."""
        for pos in self.positions:
            self.stage_move_absolute(pos) 
    
    def set_timelapse(self, frame, interval):
        """Set time-lapse settings."""
        self.timelapse_settings['frame'] = frame
        self.timelapse_settings['interval'] = interval
    
    def set_mosaic(self, rows, columns):
        """Set mosaic settings."""
        self.mosaic_settings['rows'] = rows
        self.mosaic_settings['columns'] = columns
    
    def execute(self):
        """Simulate the GO action."""
        print("Executing acquisition with the following settings:")
        print(f"Positions: {self.positions}")
        print(f"Timelapse: {self.timelapse_settings}")
        print(f"Mosaic: {self.mosaic_settings}")

    
    
    def ZStack(self, nSlices=None, step=None, path=None):
        import time
        """Perform Z-Stack acquisition."""
        nSlices = nSlices #50
        step = step #0.001
        z_start = (nSlices*step + step)/2 
        self.stage.move_relative(0, 0, z_start)
        
        path = path
        #path = "240920_ZStacks/TEST_"
        
        for s in range(nSlices):
            self.stage.move_relative(0, 0, -step)
            time.sleep(0.1)
            name = f"{path}_{s}.tif"
            self.camera.core.capture(path=name)
            time.sleep(self.camera.core.exposure/1000000 + 0.1)  # Wait for exposure
            



        
        