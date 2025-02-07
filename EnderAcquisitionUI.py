import ipywidgets as widgets
from EnderAcquisitionCore import EnderAcquisitionCore
import os

class EnderAcquisitionUI:
    def __init__(self, title="EnderAcquisition", stage=None, camera=None, lightBF=None, lightFluo=None):
        self.core = EnderAcquisitionCore(stage=stage, camera=camera)
        self.title = title
        self.lightBF=lightBF
        self.light_fluo=lightFluo
        
        # Multipos UI
        self.checkbox_multipos = widgets.Checkbox()
        self.save_button = widgets.Button(description="Save Position")
        self.delete_button = widgets.Button(description="Delete Position")
        self.reset_button = widgets.Button(description="Reset All Positions")
        self.go_button = widgets.Button(description="Go to Position")
        self.position_table = widgets.HTML("<b>Positions:</b> <br> No positions yet")
        
        # Timelapse UI
        self.checkbox_timelpase = widgets.Checkbox()
        self.frame_input = widgets.IntText(description="Frame")
        self.interval_input = widgets.FloatText(description="Interval (s)")
        
        # Mosaic UI
        self.checkbox_mosaic = widgets.Checkbox()
        self.rows_input = widgets.IntText(description="Rows")
        self.columns_input = widgets.IntText(description="Columns")

        # Z Stack
        self.checkbox_zStack = widgets.Checkbox()
        self.nSlices = widgets.IntText(description="Slices", value=1)
        self.stepSize = widgets.FloatText(description="step", value=0.1)

        # File picker
        self.file_picker = widgets.Text(
            description="Save As:",
            placeholder="Enter file path",
            value="multi-image.jpg"
        )
        
        # GO button
        self.go_acquisition_button = widgets.Button(description="GO", button_style='success')

        # OUtput message
        self.outputMessage = widgets.Text(
            value='waitng for command',
            placeholder='',
            description='',
            disabled=False  
        )

        # Setup accordion
        self.accordion = widgets.Accordion(children=[
            widgets.VBox([self.checkbox_multipos, self.save_button, self.delete_button, self.reset_button, self.go_button, self.position_table]),
            widgets.VBox([self.checkbox_timelpase, self.frame_input, self.interval_input]),
            widgets.VBox([self.checkbox_mosaic, self.rows_input, self.columns_input]),
            widgets.VBox([self.checkbox_zStack, self.nSlices, self.stepSize])
        ])
        self.accordion.set_title(0, "Multipos")
        self.accordion.set_title(1, "Timelapse")
        self.accordion.set_title(2, "Mosaic")
        self.accordion.set_title(3, "Zstack")
        
        # Attach event handlers
        self.save_button.on_click(self.on_save_position)
        self.delete_button.on_click(self.on_delete_position)
        self.reset_button.on_click(self.on_reset_positions)
        self.go_button.on_click(self.on_go_to_position)
        self.go_acquisition_button.on_click(self.on_go_acquisition)
        
    def on_save_position(self, _):
        position = f"Position {len(self.core.positions) + 1}_{self.stage.get_position()}"
        self.core.save_position(position)
        self.update_position_table()
        
    def on_delete_position(self, _):
        if self.core.positions:
            self.core.delete_position(self.core.positions[-1])
        self.update_position_table()
        
    def on_reset_positions(self, _):
        self.core.reset_positions()
        self.update_position_table()
        
    def on_go_to_position(self, _):
        if self.core.positions:
            self.core.go_to_position(self.core.positions[-1])
        
    def on_go_acquisition(self, _):
        directory = self.file_picker.value
        if not os.path.exists(directory):
            os.makedirs(directory)
            
        self.lightBF.core.toggle() #ON
        #____________________
        # MATTHIEU ACQUI INIT
        #exposure = 500000 / gain = 2
        self.light_fluo.core.set_rgb_color(0, 0, 255)
        self.light_fluo.core.set_intensity(1)
        self.lightBF.core.set_rgb_color(255, 255, 255)
        self.lightBF.core.set_intensity(1)
        self.lightBF.core.toggle() #ON
        #____________________


        
        if sel.checkbox_timelapse.value == True:
            self.outputMessage.value = "Timelpase lets_go !"
            nFrames = self.frame_input.value, 
            interval = self.interval_input.value
            self.outputMessage.value = "Time ok !"

        else:
            nFrames = 1
            interval = 1

            for frame in range(nFrames):
                if self.checkbox_multipos.value == True:
                    self.outputMessage.value = "multipos lets_go to"
                    nbPos = self.core.positions.lenth()
                else:
                    nbPos = 1
                for pos in range(nPos):
                    self.stage_move_absolute(positions[pos]) 
                    self.outputMessage.value = "positionOK"
                
                if self.checkbox_mosaic == True:
                    self.outputMessage.value = "mosaic lets_go to"
                    nbRows = self.rows_input
                    nbCols = self.columns_input
                else:
                    nbRows = 1
                    nbCols = 1
                    
                # Boucle en X
                direction = 1
                pas = 1.5
                n = nbRows
                for i in range(n**2):
                    #HERE IMAGE
                    if i%n == 0:
                        self.stage.move_relative(0,pas,0)
                        #gcode = "G0 Y"+ str(pas) + "\n"
                        direction *= -1
                    self.stage.move_relative(pas * direction,0,0)
                    #gcode = "G0 X" + str(pas * direction) + "\n"
                    if direction < 0:
                        nameMosa = "mosa_x"+str(n - i%n)+"_y"+str(i//n)+".tif"
                    else:
                        nameMosa = "mosa_x"+str(i%n)+"_y"+str(i//n)+".tif"
                    
                        # MATT SETTINGS
                        nameFLUO = os.path.join(directory, f"gfp_{number}h00_GFP_exp-{exposure}s_gain{gain}_{nameMosa}.tif")
                        nameBF = os.path.join(directory, f"gfp_{number}h00_BF_exp-{exposure}s_gain{gain}_{nameMosa}.tif")

                        self.camera.core.autofocus()
                        self.lightBF.core.toggle() #OFF
                        time.sleep(0.2)
                        self.light_fluo.core.toggle()  # Toggle light on
                        
                        time.sleep(0.2)
                        self.camera.core.capture(path=nameFLUO)
                        time.sleep(self.camera.core.exposure/1000000 + 0.1)  # Wait for exposure
                        self.light_fluo.core.toggle()  # Toggle light off
                        
                        time.sleep(0.2)
                        
                        # Capture image BF
                        self.lightBF.core.set_intensity(0.5)
                        
                        self.lightBF.core.toggle() # ON
                        time.sleep(0.2)
                        self.camera.core.capture(path=nameBF)
                        time.sleep(self.camera.core.exposure/1000000 + 0.1)  # Wait for exposure
                    
                        # WAIT Growth for 1h00 !
                        self.lightBF.core.set_intensity(1)
                        
            time.sleep(interval) #1h00
            self.lightBF.core.toggle() #OFF
            
            #Z-STACK OK
                    # if self.checkbox_zStack.value == True:
                    #     self.outputMessage.value = "Z-stack let's go"
                    #     self.core.ZStack(nSlices = self.nSlices.value, step= self.stepSize.value, path = self.file_picker.value )
                    #     self.outputMessage.value = "ZSTack ok"
                    #             # File picker
                    # else:
                    #     self.outputMessage.value = "button clicked but noting happend"

            
                #frame = self.frame_input.value
        #interval = self.interval_input.value
        #rows = self.rows_input.value
        #columns = self.columns_input.value
        #self.core.set_timelapse(frame, interval)
        #self.core.set_mosaic(rows, columns)
        #self.core.execute()

    def update_position_table(self):
        positions_html = "<br>".join(self.core.positions)
        self.position_table.value = f"<b>Positions:</b> <br> {positions_html}"
        
    def get_controls(self):
        """Return the UI components."""
        return widgets.VBox([self.accordion, self.go_acquisition_button, self.file_picker, self.outputMessage])

    def get_output(self):
        return None
    def get_title(self):
        return self.title
