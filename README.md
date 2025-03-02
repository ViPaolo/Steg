# Steg

Steg is a simple, user-friendly tool for encoding simple textual messages into an RGB image. It provides a simple user interface to encode and decode your UTF-8 encodings into the Least Significant Bit (LSB).
This tool differentiate by using RGB channels instead of single pixels, allowing thus to encode up to three times the pixel count of an image, compared to only the pixel count. 

## Repo structure. 
The repo is built around 3 folders. 

1. **src**, which contains the main python file with the necessary modules for encoding, decoding and SRC.
2. **gui**, which containes the main folder structure.
3. **test**, some tests made by pytest to check for edge cases in the src folder

## Installation

You can manually build an .exe file from the code with pyinstaller by doing the following steps:

1. Clone the repository locally.
2. (Optional) Activate a virtual environment. You can activate a virtual environment in python by using [this guide](https://docs.python.org/3/tutorial/venv.html)
3. Install the required dependencies. You can do so by simply writing `py -m pip install -r requirements.txt`
4. Run the pyinstaller. To avoid the need for dependencies, I include all of them and make a portable version with the following line (it must be run from the repo's main folder directory): `pyinstaller --name "Steg" --onefile --windowed --add-data "src;src" gui/CTgui.py`. Alternatively, you can see if there is any stable distribution on the 'releases' tab.


