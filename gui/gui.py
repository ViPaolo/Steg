import streamlit as st
import Pillow
import io
# 
# Replace with your steganography encode/decode functions
def encode_image(img, message):
    # Your existing steganography logic here
    return img

st.title("Steganography App 🔒")
uploaded_file = st.file_uploader("Upload an image", type=["png", "jpg", "jpeg"])
message = st.text_input("Secret message")

if uploaded_file and message:
    image = Image.open(uploaded_file)
    encoded_image = encode_image(image, message)  # Use your function here
    
    # Show preview
    st.image(encoded_image, caption="Encoded Image")
    
    # Download button
    buf = io.BytesIO()
    encoded_image.save(buf, format="PNG")
    st.download_button("Download Image", buf.getvalue(), "secret_image.png")

