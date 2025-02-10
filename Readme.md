Enderscope Microscopy

Enderscope Microscopy is a modular Python library derived from the Enderscope project. It enables communication with the Enderscope, a DIY, budget-friendly microscope system that repurposes a 3D printer into an automated imaging tool. The system primarily runs on a Raspberry Pi, utilizing an HQ camera and Neopixel LEDs.

Features

Modular system: Works with various Enderscope modules like EnderPiLight, EnderPiCam, EnderStage, and more.

Flexible UI with EnderPanel: Automatically generates a customizable interface based on the provided modules.

Jupyter Notebook support: The system can run interactively within Jupyter Notebooks.

Automated imaging: Easily configure and automate microscope functions using Python.

Seamless integration with Raspberry Pi: Designed for embedded systems with efficient hardware communication.

Installation

pip install board, serial, neopixels,

Usage

To create a modular interface using EnderPanel, simply import and initialize with the desired modules:

from enderscope_microscopy import EnderPanel, EnderPiLight, EnderPiCam, EnderStage

enderMain = EnderPanel(EnderStage(), EnderPiCam(), EnderPiLight("LED1"), EnderPiLight("LED2"))
enderMain.run()

This setup automatically adds tabs in the interface corresponding to each module, allowing for an adaptable and interactive microscopy experience.

Components

EnderPiLight: Controls Neopixel LED illumination.

EnderPiCam: Manages camera settings and image capture.

EnderStage: Controls motorized stage movements.

EnderPanel: Dynamically generates a UI based on included modules.

Why Use Enderscope Microscopy?

Highly customizable: Easily add or remove modules to match your imaging needs.

Open-source and DIY-friendly: Perfect for makers, researchers, and educators.

Integrated automation: Control imaging conditions and workflows programmatically.

Contributing

Contributions are welcome! Feel free to submit pull requests or open issues.

License

This project is licensed under the MIT License.

Acknowledgments

Enderscope Microscopy is inspired by Enderscope, an innovative project transforming 3D printers into advanced, flexible microscopy tools.

