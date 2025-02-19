# Enderscope Microscopy Adaptation

## About
This project is an adaptation of the [original EnderScope project](https://github.com/Pickering-Lab/EnderScope), specifically optimized for epifluorescence microscopy with a 10X objective. While the original EnderScope transforms an Ender 3D printer into a versatile imaging system, this adaptation focuses on biological applications and microscopy capabilities.

## Original Project Credit
This work is based on the EnderScope project developed by the Pickering Lab. The original project can be found at: https://github.com/Pickering-Lab/EnderScope

## Modifications and Improvements
This adaptation includes:
- Specialized setup for epifluorescence microscopy
- Optimized for 10X objective use
- Enhanced biological sample imaging capabilities
- Custom Python scripts for microscopy-specific functions

## Required Hardware
- Ender 3D printer (system base)
- Raspberry Pi
- Raspberry Pi HQ Camera
- Neopixel UltraBirght 4W LEDs
- 10X microscope objective
- 3D printed parts
- optical lens in PMMA


## Installation and Setup
1. Print the necessary 3D parts (files available in the `3D_pieces` directory)
2. Assemble the system according to the assembly guide (coming soon...)
3. Configure the Raspberry Pi
4. Install the required Python dependencies


## Python dependencies
```bash
pip install board
pip install serial
pip install neopixel
```

## Usage
```python
from enderscope_microscopy import EnderPanel, EnderPiLight, EnderPiCam, EnderStage

# Initialize components
enderMain = EnderPanel(
    EnderStage(),
    [EnderPiCam(title = "myCam"),
    EnderPiLight(title = "LED1"),
    EnderPiLight(title ="LED2")]
)

# Launch interface
enderMain.run()
```

## Available Modules
- **EnderStage**: Motorized movement control
- **EnderPanel**: Modular user interface
- **EnderPiLight**: LED illumination control
- **EnderPiCam**: Camera management


## Contributing
Contributions are welcome! Feel free to:
- Submit pull requests
- Report bugs
- Suggest improvements
- Share your modifications

## License
This project is licensed under the GPL v3 License.


## Acknowledgments
- Original EnderScope project by the Pickering Lab (https://github.com/Pickering-Lab/EnderScope)
- EnderSchool's Team (Jerôme et Erwan !)
- Open-source community for their continuous support