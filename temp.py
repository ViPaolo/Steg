try:
    import numpy as np
    from PIL import Image
    import os
    import sys
except ImportError as e:
    raise ImportError(f"Missing dependencies: {e}. Install them with 'pip install -requirements.txt'")









def Encode_Image(img: Image.Image, txt : str) -> Image.Image:
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
        raise ValueError("The Image is not in RGB format")

    #Transforms the pixel in a matrix containing 3-vector values. 
    pixels = np.array(img)
    height, width, _ = pixels.shape

    #Encode message in bytes
    txt_bin = txt.encode('utf-8') + b'\x00' #Terminating bit
    #The code is already converted (internally, we'll se a sequence of byte), 
    # but to represent them in a sequence of bits (and not int) we need to convert them in a binary string.  
    txt_bits = "".join(f'{byte:08b}' for byte in txt_bin) #byte:08b ensures each type is represented in exactly 8 bits. 


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
                    #254 is 11111110, so the bitwise AND clears the LSB
                    #txt_bits[bit_count] returns the i-th bit, the OR operation then will be between 
                    # original pixel channel OR original bit (00000001 or 00000000)
                    #If then 
                    rd= (rd & 254) | int(txt_bits[bit_count]) 
                    bit_count += 1
                if bit_count < len(txt_bits):
                    gr = (gr & 254) | int(txt_bits[bit_count])
                    bit_count += 1
                if bit_count < len(txt_bits):
                    bl = (bl & 254) | int(txt_bits[bit_count])
                    bit_count += 1

                pixels[h,w] = (rd,gr,bl)
            



    new_img = Image.fromarray(pixels, "RGB")
    return new_img


def Decode_Image(img : Image.Image) -> str:

    #The image encoded with this method should be natively RGB. However, the user may have changed some options or encoding. 
    #It is with the philosophy of allowing the user to use it in changing the image.
    # Provided the user has only changed the reading mode but not the photo per se, the message should remain valid. 
    if img.mode != "RGB":
        img = img.convert("RGB")
        

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



#Generate Image 



img = Image.open(os.path.join(os.path.dirname(__file__), r"Lenna.png"))
print(img)

encoded = Encode_Image(img, "OH MA COME TI PERMETTI.")

encoded.convert("CMYK")

encoded.convert("RGB")

decoded = Decode_Image(encoded)
print(decoded)

n1 = np.array([1,2,1])
n2 = np.array([1,2,1])
if np.array_equal(n1, n2):
    print(True)
else:
    print(False)

pixels = np.array(img)

print(pixels.shape)



# print(decoded)

