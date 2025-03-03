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
        #self.set_relative()
        self.position = {'x': 0.0, 'y': 0.0, 'z': 0.0}
        self.sensitivityXY = 1.0  # Default sensitivity value
        self.sensitivityZ = 0.1  # Default sensitivity value

        # Sensitivity slider for XY
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

        # Sensitivity slider for Z
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

        # Text area to display logs/output
        self.output_area = widgets.Textarea(
            value='',
            placeholder='Logs will appear here...',
            description='Output:',
            layout=widgets.Layout(width='100%', height='100px')
        )

    def log(self, message):
        """Helper function to log messages to the TextArea."""
        self.output_area.value += f"{message}\n"
        self.output_area.scroll_to_bottom()

    def write_code(self, code, check_ok=True, debug=False):
        self.log(f"Sending command: {code}")
        super().write_code(code)
        response = self.serial.readline().decode('utf-8')
        if check_ok:
            while not response.startswith("ok"):
                if debug:
                    self.log(response.strip('\n'))
                response = self.serial.readline().decode('utf-8')
        if debug:
            self.log(f"Response: {response.strip()}")
        return response

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
        self.log(f"Moved to relative position: X={self.position['x']}, Y={self.position['y']}, Z={self.position['z']}")

    def move_absolute(self, x, y, z=None, debug=False):
        self.set_absolute()
        if z is None:
            code = f"G0 X {x} Y {y}"
        else:
            code = f"G0 X {x} Y {y} Z {z}"
        self.write_code(code, debug=debug)
        self.position = {'x': x, 'y': y, 'z': z if z is not None else self.position['z']}
        self.log(f"Moved to absolute position: X={x}, Y={y}, Z={self.position['z']}")

    def home(self, debug=False):
        self.write_code('G28', debug=debug)
        self.position = {'x': 0.0, 'y': 0.0, 'z': 0.0}
        self.log("Homed stage to origin (0, 0, 0)")

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
                self.log("Error: Invalid numeric values for X, Y, and Z")

        x_input = create_simple_floattext('X:', self.position['x'])
        y_input = create_simple_floattext('Y:', self.position['y'])
        z_input = create_simple_floattext('Z:', self.position['z'])

        go_button = widgets.Button(
            layout=widgets.Layout(width='240px', height='30px', padding='2px'),
            tooltip="Go to position",
            icon='location-arrow',
            button_style='primary',
            style={'button_color': '#d3d3d3'}
        )
        go_button.on_click(move_stage_to_position)

        # Directional movement buttons
        north_button = create_icon_button('arrow-up', 'Move North', 'lightblue')
        south_button = create_icon_button('arrow-down', 'Move South', 'lightblue')
        west_button = create_icon_button('arrow-left', 'Move West', 'lightblue')
        east_button = create_icon_button('arrow-right', 'Move East', 'lightblue')
        home_button = create_icon_button('home', 'Home', 'salmon')
        up_button = create_icon_button('arrow-up', 'Move Up (Z+)', 'lightgreen')
        down_button = create_icon_button('arrow-down', 'Move Down (Z-)', 'lightgreen')

        # Button actions
        north_button.on_click(lambda b: self.move_relative(0, 1 * self.sensitivityXY))
        south_button.on_click(lambda b: self.move_relative(0, -1 * self.sensitivityXY))
        west_button.on_click(lambda b: self.move_relative(-1 * self.sensitivityXY, 0))
        east_button.on_click(lambda b: self.move_relative(1 * self.sensitivityXY, 0))
        home_button.on_click(lambda b: self.home())
        up_button.on_click(lambda b: self.move_relative(0, 0, 1 * self.sensitivityZ))
        down_button.on_click(lambda b: self.move_relative(0, 0, -1 * self.sensitivityZ))

        # Layout for movement controls
        movement_controls = widgets.GridBox(
            children=[
                widgets.Label(),  # (0, 0) Empty
                north_button,  # (0, 1)
                widgets.Label(),  # (0, 2) Empty
                widgets.Label(),  # (0, 3) Empty
                up_button,  # (0, 4)

                west_button,  # (1, 0)
                widgets.Label(),  # (1, 1)
                east_button,  # (1, 2)
                widgets.Label(),  # (1, 3) Empty
                down_button,  # (1, 4)

                widgets.Label(),  # (2, 0) Empty
                south_button,  # (2, 1)
                widgets.Label(),  # (2, 2) Empty
                widgets.Label(),  # (2, 3) Empty
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
        sensitivityXY_controls = widgets.VBox([self.sensitivityXY_slider])
        sensitivityZ_controls = widgets.VBox([self.sensitivityZ_slider])

        # Main control widget
        control_widget = widgets.VBox([
            movement_controls,
            sensitivityXY_controls,
            sensitivityZ_controls,
            position_controls
        ])

        # Return final layout including the output area
        final_layout = widgets.VBox([
            control_widget,
            self.output_area
        ])
        return final_layout

    def update_sensitivityXY(self, change):
        self.sensitivityXY = change['new']
        self.log(f"Updated XY sensitivity: {self.sensitivityXY}")

    def update_sensitivityZ(self, change):
        self.sensitivityZ = change['new']
        self.log(f"Updated Z sensitivity: {self.sensitivityZ}")

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