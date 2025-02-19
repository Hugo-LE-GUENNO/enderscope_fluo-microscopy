# 🔬 💡 Enderscope Microscopy Adaptation 💡 🔬

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

## Required Components

| Component                            | Source/Link                              | Price (February 2025) | Notes                   |
|--------------------------------------|-----------------------------------------|----------------------|-------------------------|
| HQ CAM pi                            | [Kubii](https://www.kubii.com/fr/cameras-capteurs/2950-camera-hq-officielle-5056561800127.html) | €58                 |                         |
| Raspberry Pi 4                       | [RaspberryPi](https://www.raspberrypi.com/products/raspberry-pi-4-model-b/) | €35                 |                         |
| LED ultra bright 4W                  | [Adafruit](https://www.adafruit.com/product/5408) | €5.5               |                         |
| Objective 10X RMS                    | [Naturoptic 10x Objective](https://www.naturoptic.com/detail-objectif-microscope-10x-160--146.php) | €35 | Prefer reusing if possible! 🔄 🌱|
| Dichroic Filters (excitation + dual + emission) | [Evident Scientific Fluorescence Filters](https://evidentscientific.com/en/microscope-resource/knowledge-hub/techniques/fluorescence/filters) | ~€    | Prefer reusing if possible! 🔄 🌱 |
| Ender-3 3D Printer                   | [Creality](https://www.creality.com/products/ender-3-3d-printer) | €189               |                         |
| PMMA plano-convex optical lens       | [AliExpress (lot de 100)](https://fr.aliexpress.com/i/32242266574.html?gatewayAdapt=glo2fra) | €32                 |                         |




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


## Acknowledgments 👋 👋 👋 
- Original EnderScope project by the Pickering Lab (https://github.com/Pickering-Lab/EnderScope)
- EnderSchool's Team (Jerôme et Erwan !)
- Open-source community for their continuous support