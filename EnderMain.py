import serial
from serial_utils import SerialDevice, serial_ports
import ipywidgets as widgets
from IPython.display import display

G_CODES = {
    'absolute': 'G90',
    'relative': 'G91',
    'homing': 'G28',
    'finish': 'M400',
    'current_position': 'M114'
}
DIRECTION_PREFIXES = {
    "north": "Y",
    "south": "Y-",
    "east": "X",
    "west": "X-",
    "up": "Z",
    "down": "Z-"
}



class Stage(SerialDevice):
    def __init__(self, port, baud_rate=115200, parity=serial.PARITY_NONE,
                 stop_bits=serial.STOPBITS_ONE, byte_size=serial.EIGHTBITS):
        super().__init__(port, baud_rate, parity, stop_bits, byte_size)
        self.set_relative()
        self.position = {'x': 0.0, 'y': 0.0, 'z': 0.0}
        self.sensitivityXY = 1.0  # Default sensitivity value
        self.sensitivityZ = 0.1  # Default sensitivity value
        
        # Sensitivity slider
        self.sensitivityXY_slider = widgets.FloatSlider(
            value=self.sensitivityXY,
            min=0.01,
            max=10.0,
            step=0.01,
            description='Sensitivity XY:',
            continuous_update=True,
            style={'description_width': 'initial'}
        )
        self.sensitivityXY_slider.observe(self.update_sensitivityXY, names='value')

        # Sensitivity slider
        self.sensitivityZ_slider = widgets.FloatSlider(
            value=self.sensitivityZ,
            min=0.01,
            max=2.0,
            step=0.01,
            description='Sensitivity Z:',
            continuous_update=True,
            style={'description_width': 'initial'}
        )
        self.sensitivityZ_slider.observe(self.update_sensitivityZ, names='value')

    def get_position(self, dict=False, debug=False):
        self.flush_serial_buffer()
        response = self.write_code(G_CODES['current_position'],
                                   check_ok=False)
        if debug:
            print(response)
        ok = self.serial.readline()
        if not ok.decode('utf-8').startswith("ok"):
            print("Error reading stage position")
            return
        position = response.split(" Count")[0]
        parts = position.split()
        positions = {part.split(":")[0]: float(part.split(":")[1]) for part in parts}
        if dict==False:
            order = ['X','Y', 'Z']
            positions = tuple([positions[field] for field in order])
        return positions

    
    def update_sensitivityXY(self, change):
        """Update the sensitivity based on slider value."""
        self.sensitivityXY = change['new']
        print(f"Stage sensitivity set to {self.sensitivityXY:.2f}")

    def update_sensitivityZ(self, change):
        """Update the sensitivity based on slider value."""
        self.sensitivityZ = change['new']
        print(f"Stage sensitivity set to {self.sensitivityZ:.2f}")

    def write_code(self, code, check_ok=True, debug=False):
        super().write_code(code)
        response = self.serial.readline().decode('utf-8')
        if check_ok:
            while not response.startswith("ok"):
                if debug:
                    print(response.strip('\n'))
                response = self.serial.readline().decode('utf-8')
        if debug:
            print(code)
        return response

    def temp(self, temp, debug=False):
        code = f"M190 S{temp-1} R{temp+1}"
        self.write_code(code, debug=debug)
        
    def move_absolute(self, x, y, z=None, debug=False):
        self.set_absolute()
        if z is None:
            code = f"G0 X {x} Y {y}"
        else:
            code = f"G0 X {x} Y {y} Z {z}"
        self.write_code(code, debug=debug)
        self.position = {'x': x, 'y': y, 'z': z if z is not None else self.position['z']}

    def move_relative(self, x, y, z=None, debug=False):
        self.set_relative(debug=debug)
        if z is None:
            code = f"G0 X {x} Y {y}"
        else:
            code = f"G0 X {x} Y {y} Z {z}"
        self.write_code(code, debug=debug)
        self.position['x'] += x
        self.position['y'] += y
        if z is not None:
            self.position['z'] += z

    def home(self, debug=False):
        self.write_code('G28', debug=debug)
        self.position = {'x': 0.0, 'y': 0.0, 'z': 0.0}

    def set_relative(self, debug=False):
        self.write_code('G91', debug=debug)

    def set_absolute(self, debug=False):
        self.write_code('G90', debug=debug)

    def get_controls(self):
        def create_icon_button(icon, description, color):
            button = widgets.Button(
                layout=widgets.Layout(width='40px', height='40px', padding='1px'),
                tooltip=description,
                icon=icon,
                button_style='primary'
            )
            button.style.button_color = color
            return button

        def create_simple_floattext(description, value):
            floattext = widgets.FloatText(
                description=description,
                value=value,
                layout=widgets.Layout(width='80px', height='30px'),
                style={'description_width': 'initial'}
            )
            return floattext

        def move_stage_to_position(b):
            try:
                x = float(x_input.value)
                y = float(y_input.value)
                z = float(z_input.value)
                self.move_absolute(x, y, z)
            except ValueError:
                print("Please enter valid numeric values for X, Y, and Z.")

        x_input = create_simple_floattext('X:', self.position['x'])
        y_input = create_simple_floattext('Y:', self.position['y'])
        z_input = create_simple_floattext('Z:', self.position['z'])

        go_button = widgets.Button(
            layout=widgets.Layout(width='240px', height='30px', padding='2px'),
            tooltip="Go to position",
            icon='location-arrow',  # Updated icon
            button_style='primary',  # No pre-set style to allow custom color
            style={'button_color': '#d3d3d3'}  # Dark gray color for the button
        )
        go_button.on_click(move_stage_to_position)

        north_button = create_icon_button('arrow-up', 'Move North', 'lightblue')
        south_button = create_icon_button('arrow-down', 'Move South', 'lightblue')
        west_button = create_icon_button('arrow-left', 'Move West', 'lightblue')
        east_button = create_icon_button('arrow-right', 'Move East', 'lightblue')
        home_button = create_icon_button('home', 'Home', 'salmon')
        up_button = create_icon_button('arrow-up', 'Move Up (Z+)', 'lightgreen')
        down_button = create_icon_button('arrow-down', 'Move Down (Z-)', 'lightgreen')

        north_button.on_click(lambda b: self.move_relative(0, 1*self.sensitivityXY))
        south_button.on_click(lambda b: self.move_relative(0, -1*self.sensitivityXY))
        west_button.on_click(lambda b: self.move_relative(-1*self.sensitivityXY, 0))
        east_button.on_click(lambda b: self.move_relative(1*self.sensitivityXY, 0))
        home_button.on_click(lambda b: self.home())
        up_button.on_click(lambda b: self.move_relative(0, 0, 1*self.sensitivityZ))
        down_button.on_click(lambda b: self.move_relative(0, 0, -1*self.sensitivityZ))

        movement_controls = widgets.GridBox(
            children=[
                widgets.Label(),  # (0, 0) Vide
                north_button,  # (0, 1)
                widgets.Label(),  # (0, 2) Vide
                widgets.Label(),  # (0, 3) Vide
                up_button,  # (0, 4)

                west_button,  # (1, 0)
                widgets.Label(), # (1, 1)
                east_button,  # (1, 2)
                widgets.Label(),  # (1, 3) Vide
                down_button,  # (1, 4)

                widgets.Label(),  # (2, 0) Vide
                south_button,  # (2, 1)
                widgets.Label(),  # (2, 2) Vide
                widgets.Label(),  # (2, 3) Vide
                home_button, 
            ],
            layout=widgets.Layout(
                grid_template_columns='repeat(5, 30px)',
                grid_template_rows='repeat(3, 45px)',
                grid_gap='5px',
                justify_content='center',
                align_items='center'
            )
        )
         # Layout for position controls
        position_controls = widgets.VBox([
            widgets.HBox([x_input, y_input, z_input], layout=widgets.Layout(padding='5px')),
            go_button
        ], layout=widgets.Layout(padding='10px', align_items='center'))

        # Sensitivity slider controls
        sensitivityXY_controls = widgets.VBox([
            self.sensitivityXY_slider
        ])
        # Sensitivity slider controls
        sensitivityZ_controls = widgets.VBox([
            self.sensitivityZ_slider
        ])

        # Combine everything into the main layout
        return widgets.VBox([
            widgets.Label(value=""),
            movement_controls,
            position_controls,
            sensitivityXY_controls,
            sensitivityZ_controls
        ])

    def get_output(self):
        return None

    def has_output(self):
        return False


class Panel:
    def __init__(self, stage, components):
        self.stage = stage
        self.components = components
        self.create_ui()

    def create_ui(self):
        # Input tabs in the middle
        input_tabs = widgets.Tab()
        input_controls = []
        input_titles = []

        for component in self.components:
            if hasattr(component, 'get_controls') and component.get_controls() is not None:
                input_controls.append(component.get_controls())
                input_titles.append(component.get_title() if hasattr(component, 'get_title') else component.__class__.__name__)
        
        input_tabs.children = input_controls
        for i, title in enumerate(input_titles):
            input_tabs.set_title(i, title)
        
        # Output tabs on the right
        output_tabs = widgets.Tab()
        output_controls = []
        output_titles = []

        for component in self.components:
            if hasattr(component, 'get_output') and component.get_output() is not None:
                output_controls.append(component.get_output())
                output_titles.append(component.get_title() if hasattr(component, 'get_title') else component.__class__.__name__)
        
        output_tabs.children = output_controls
        for i, title in enumerate(output_titles):
            output_tabs.set_title(i, title)

        # Layout setup
        self.ui = widgets.HBox([self.stage.get_controls(), input_tabs, output_tabs])

    def display(self):
        display(self.ui)