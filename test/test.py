## TO RUN THE PYTEST, after you have installed the pytest package, simply run: 
    # pytest Test/test.py in the root folder. 

#to run the package, pytest requires the name of the package to be 

try:
    import numpy as np
    from PIL import Image
    import pytest
    import math
#We need to import also the functions:
    from src.steg import Encode_Image,Decode_Image,PSNR  #relative import, use it only if you install the repo as package!

except ImportError as e:
    raise ImportError(f"The following module cannot be imported: {e}. Install the required dependencies with 'pip install -r requirements.txt'. ")


def test_encode_decode_ascii():
    """
    Test basic ASCII encoding with a generated white image.

    Input: A 20x20 white RGB photo. 
    Text: "Ciao, amole."

    """

    img = Image.new("RGB", (20,20), color="white")
    message = "Ciao, amole."

    encoded_img = Encode_Image(img, message)
    decoded_message = Decode_Image(encoded_img)

    assert decoded_message == message

def test_encode_decode_non_ascii():
    """
    Test if UTF-8 encoding with non-ASCII character works, with a generated white image.

    Input: A 40x40 RGB white photo. 
    Text: "こんにちは世界"

    """

    img = Image.new("RGB", (40,40), color="white")
    message = "こんにちは世界"

    encoded_img = Encode_Image(img, message)
    decoded_message = Decode_Image(encoded_img)

    assert decoded_message == message

def test_encode_decode_emoji():
    """
    
    Test if UTF-8 encoded emoji works, with a generated white image.

    Input: A 20x20 RGB white Photo.
    Text: "😊". Expected 5 bytes.

    """
    img = Image.new("RGB", (40,40), color="white")
    message = "😊"

    encoded_img = Encode_Image(img, message)
    decoded_message = Decode_Image(encoded_img)

    assert decoded_message == message



def test_empty_message():

    """

    Test encoding and decoding an empty message in a white message.
    
    Input: A 10x10 RGB white photo. 
    Text: ""

    """
    img = Image.new("RGB", (10, 10), color="white")
    message = ""
    encoded_img = Encode_Image(img, message)
    decoded_message = Decode_Image(encoded_img)
    assert decoded_message == message


def test_ascii_message_too_large():
    """
    
    Test that encoding a message too large for the image raises an error.
    
    Input: A 1x1 Immage

    Text: "Ciao, tesoro."
    
    Should raise a ValueError.


    """
    
    img = Image.new("RGB", (1, 1), color="white")
    message = "Ciao, tesoro."

    # "e use the context manager to capture the ValueError with the Pytest method.
    #  We use with as context manager because we expect an error and then close the process.
    with pytest.raises(ValueError):
        Encode_Image(img, message)

def test_non_ascii_message_too_large():
    """
    Test that a non-ASCII message (which may have multi-byte characters) that
    exceeds the image capacity raises a ValueError.

    Input: 4x4 RGB image.
    Text: "😊😊",  which are 9 bytes including the terminating byte. 

    Should raise a ValueError.
    """
    
    img = Image.new("RGB", (4, 4), color="white")
    message = "😊😊"
    with pytest.raises(ValueError):
        Encode_Image(img, message)



def test_non_rgb_image_conversion():
    """
    Test a greyscale but convertible image, to check if it's possibleto check it.
    
    Input: A 20x20 Greyscale Image.

    Text: "Ciao, tesoro."

    """

    img = Image.new("L", (20, 20), color="white")
    message = "Ciao, tesoro."

    encoded_img = Encode_Image(img, message)
    # The resulting image should be in RGB mode
    assert encoded_img.mode == "RGB"
    decoded_message = Decode_Image(encoded_img)
    assert decoded_message == message

def test_invalid_utf8():
    """
    Test decoding an image with an invalid UTF-8 sequence raises a ValueError.
    
    """
    # Create a small image array manually.
    arr = np.zeros((2, 2, 3), dtype=np.uint8)
    flat = arr.flatten()

    # Set the first 8 LSBs to 1, forming the byte 0xFF,
    # which is an invalid stand-alone UTF-8 byte.
    for i in range(8):
        flat[i] |= 1
    arr = flat.reshape((2, 2, 3))
    img_invalid = Image.fromarray(arr, "RGB")

    with pytest.raises(ValueError):
        Decode_Image(img_invalid)

def test_maximum_capacity_message():
    """
    Test encoding a message that exactly uses up the available capacity.
    For an image with N pixels (each with 3 channels), the maximum number of bytes
    that can be encoded is (N*3 // 8) - 1 (subtracting one for the termination byte).

    Input: a 4x4 image. Total message byte = 4*4*3 = 48//8 = 6-1 = 5 bytes.
    Text: "Honey" , 5 ASCII characters and 5 bytes
    """

    img = Image.new("RGB", (4, 4), color="white")
    message = "Honey"
    encoded_img = Encode_Image(img, message)
    decoded_message = Decode_Image(encoded_img)
    assert decoded_message == message

def test_psnr_equal_images():
    """
    
    Test for psnr, it compares two equal images and returns its psnr.


    Input_image: a 10x10 white image. 
    New_image: a 10x10 white image. 

    The test is passed a PSNR equal infinite, as the MSE (denominator) is zero. 

    """

    img = Image.new("RGB", (10,10), color="white")
    img2 = img
    
    psnr = PSNR(img, img2)

    assert psnr == float('inf')


def test_psnr_opposite_images():
    """
    
    Test for psnr, it compares a black and white image and returns its psnr.

    Input_image: a 10x10 white image. 
    New_image: a 10x10 black image. 

    The test is passed if the PSNR equals 0.

    """

    img = Image.new("RGB", (10,10), color="white")
    img2 = Image.new("RGB", (10,10), color="black")

    

    psnr = PSNR(img, img2)

    assert psnr == 0



if __name__ == "__main__":
    test_encode_decode_ascii() 
    test_encode_decode_non_ascii()
    test_encode_decode_emoji()
    test_empty_message()
    test_ascii_message_too_large()
    test_non_ascii_message_too_large()
    test_non_rgb_image_conversion()
    test_invalid_utf8()
    test_maximum_capacity_message()
    test_psnr_equal_images()
    test_psnr_opposite_images()
    print("All tests passed!")
