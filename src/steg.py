try:
    import numpy as np
    from PIL import Image
    import os
    import sys
except ImportError as e:
    raise ImportError(f"Missing dependencies: {e}. Install them with 'pip install -r requirements.txt'")

def encode_image(img: Image.Image, txt : str) -> Image.Image:
    """
    Embed a message on LSB of the image. 

    Parameters: 
            Image(Image.Image): The input image.

            txt(str): The text we want to include in UTF-8 encoding. The length of the text must not be larger than the HxWx3.

    

    Returns: 
        Image(Image.Image): The new image with the encoded message.

        The lenght of the text cannot be larger than three times the pixels in the image.

    """

    #check if img is RGB 
    try:
        if img.mode != "RGB":
            img = img.convert("RGB")
    except:
        raise ValueError("The Image is not in RGB format nor it can be converted. Please use another image.")

    #Transforms the pixel in a matrix containing 3-vector values. 
    pixels = np.array(img)
    height, width, _ = pixels.shape

    #Encode message in bytes
    txt_bin = txt.encode('utf-8') + b'\x00' #Terminating bit

    #The code is already converted (internally, we'll se a list of byte), 
    # but to represent them in a sequence of bits (and not int) we need to convert them in a binary string.  
    txt_bits = "".join(f'{byte:08b}' for byte in txt_bin) #byte:08b ensures each type is represented in exactly 8 bits. 

    #Preliminary check to see if the message can be contained in the image
    if len(txt_bits) > height * width * 3:
        raise ValueError("The image is too small to contain the message in the UTF Encoding. Choose another image or make this one larger.")

    #Counter of how many bit we parsed
    bit_count = 0
    for h in range(height):
        if bit_count >= len(txt_bits):
            break
        for w in range(width):
            if bit_count >= len(txt_bits):
                break 
            else:
                #extract the channel.
                rd, gr, bl = pixels[h, w]
                if bit_count < len(txt_bits):

                    #254 is 11111110, so the bitwise AND clears and set the LSB to 0
                    #txt_bits[bit_count] returns the i-th bit, the OR operation then will be between 
                    # original pixel channel OR original bit (00000001 or 00000000), if the i-th bit is zero, then the code will start to make them appear.  
                    
                    rd= (rd & 254) | int(txt_bits[bit_count])
                    bit_count += 1
                if bit_count < len(txt_bits):
                    gr = (gr & 254) | int(txt_bits[bit_count])
                    bit_count += 1
                if bit_count < len(txt_bits):
                    bl = (bl & 254) | int(txt_bits[bit_count])
                    bit_count += 1

                pixels[h,w] = (rd,gr,bl)
            



    new_img = Image.fromarray(pixels, "RGB") #Recreate the new image
    return new_img


def decode_image(img : Image.Image) -> str:

    """
    Decode a text message from the LSBs of the image. 

    Parameters: 
            Image(Image.Image): The input image.
            

    Returns: 
        text: The text from the devised message.

    Note that, although some checks can be made to , it may output valid strings although the image had not been encoded yet. 
    Use only with images you have the 
    """

    #The image encoded with this method should be natively RGB. However, the user may have changed some options ordencoding. 
    #It is with the philosophy of allowing the user to use it in changing the image. 
    
    try:
        if img.mode != "RGB":
            img = img.convert("RGB")
    except:
            raise ValueError("The Image is not in RGB format nor it can be converted. Please use another image.")

        

    pixels = np.array(img)
    height, width, _ = pixels.shape


    text_bits = '' #the bitstring

    for h in range(height):
        for w in range(width):
                rd, gr, bl = pixels[h, w]
                if rd%2 == 0: #If the value is even, the LSB must be 0, if not, add 1
                    text_bits = text_bits + "0"
                else:
                    text_bits = text_bits + "1"
                if gr%2 == 0:
                    text_bits = text_bits + "0"
                else:
                    text_bits = text_bits + "1"
                if bl%2 == 0:
                    text_bits = text_bits + "0"
                else:
                    text_bits = text_bits + "1"

    decoded_bytes = [] #UTF stores its characters in bytearray
    for i in range(0,len(text_bits),8):
        byte = text_bits[i:i+8]
        if len(byte) <8:
            break
        decoded_byte = int(byte,2) #2 denotes the base of the numerical system, in this case binary
        if decoded_byte == 0:
            break
        decoded_bytes.append(decoded_byte)

    try:
        message = bytes(decoded_bytes).decode('utf-8')
    except UnicodeDecodeError as e:
        raise ValueError(f"Error decoding message. Invalid UTF-8 sequence: {e}")
        
    return message

def PSNR(original_img, new_img):

    o_pixels = np.array(original_img).astype(np.float64) #Declaring the type of the image made the test pass. Idk why, something with the data types probably. We need to investigate further. 
    n_pixels = np.array(new_img).astype(np.float64)
    
    # Compute Mean Squared Error (MSE)
    mse = np.mean((o_pixels - n_pixels) ** 2)

    if mse == 0:
        return float('inf')  # No error => infinite PSNR
    
    # Max possible pixel value

    s = 255.0

    #PSNR formula
    psnr = 20 * np.log10(s / np.sqrt(mse))
    return psnr
                    


            
