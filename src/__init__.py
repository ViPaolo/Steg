## __init__.py allows the functions and classes created with steg.py to be used in any . It actually mark directories as Python package directories. 
## WARNING: NEVER CREATE FUNCTIONS WITH THE SANE NAME OF OFFICIAL PYPI TO AVOID AMBIGUITY.

from .steg import encode_image, decode_image, psnr

# Define what is going to be exported when someon do "from image_processing import *"

__all__ = [
    encode_image,
    decode_image,
    psnr
]