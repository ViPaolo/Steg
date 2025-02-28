import customtkinter as ctk
from tkinter import filedialog, messagebox
import os
from PIL import Image
## TO RUN IT WITHOUT PROBLEMS, ensure __init__.py exists in the src folder and run it from the root folder with 'python gui\CTgui.py' in windows or 'python gui/CTgui.py' 
from src.steg import encode_image, decode_image, psnr  # Assuming these functions are in steganography.py


class SteganographyGUI(ctk.CTk):
    def __init__(self):
        #import all attributes from CTk
        super().__init__()
        #Define basic attributes and widget.
        self.title("Image Steganography Tool")
        self.geometry("630x700")


        # Input Frame
        self.input_frame = ctk.CTkFrame(self) #Createa a background frame
        self.input_frame.pack(padx=20, pady=10, fill="x") # Aiuto, sono così negativo, veramente. 
        
        ctk.CTkLabel(self.input_frame, text="Input Image:").pack(anchor="w") #
        
        self.input_entry = ctk.CTkEntry(self.input_frame, width=400) #Entry for the input
        self.input_entry.pack(side="left", padx=(0, 10)) 
        
        self.browse_input_btn = ctk.CTkButton(self.input_frame, text="Browse", command=self.browse_input)
        self.browse_input_btn.pack(side="right")
        
        # Output Frame
        self.output_frame = ctk.CTkFrame(self) #Frame for the output path
        self.output_frame.pack(padx=20, pady=10, fill="x")
        
        ctk.CTkLabel(self.output_frame, text="Output Location:").pack(anchor="w")
        
        self.output_entry = ctk.CTkEntry(self.output_frame, width=400)
        self.output_entry.pack(side="left", padx=(0, 10))
        
        self.browse_output_btn = ctk.CTkButton(self.output_frame, text="Browse", command=self.browse_output) #Button to press the new buttom
        self.browse_output_btn.pack(side="right")
        
        # Same Output Checkbox
        self.same_output_var = ctk.BooleanVar() 
        self.same_output_checkbox = ctk.CTkCheckBox(
            self, 
            text="Use same directory as input",
            variable=self.same_output_var,
            command=self.toggle_output_entry #Disables the button if the box is checked or not. 
        )

        self.same_output_checkbox.pack(padx=20, pady=5, anchor="w")
        
        # Message Frame
        self.message_frame = ctk.CTkFrame(self)
        self.message_frame.pack(padx=20, pady=10, fill="x")
        
        ctk.CTkLabel(self.message_frame, text="Message:").pack(anchor="w")
        
        self.message_text = ctk.CTkTextbox(self.message_frame, height=100)
        self.message_text.pack(fill="x", padx=5, pady=5)
        
        # Operation Selection
        self.operation_var = ctk.StringVar(value="encode") 
        
        self.operation_frame = ctk.CTkFrame(self)
        self.operation_frame.pack(padx=20, pady=10, fill="x")
        
        #This creates the actual button
        self.encode_radio = ctk.CTkRadioButton(
            self.operation_frame,
            text="Encode",
            variable=self.operation_var,
            value="encode"
        )
        self.encode_radio.pack(side="left", padx=20)
        
        #Decode button. 
        self.decode_radio = ctk.CTkRadioButton(
            self.operation_frame,
            text="Decode",
            variable=self.operation_var,
            value="decode"
        )
        self.decode_radio.pack(side="left", padx=20)
        
        # Convert Button
        self.convert_btn = ctk.CTkButton(
            self,
            text="Convert",
            command=self.process_image,
            height=40
        )
        self.convert_btn.pack(pady=20)
        
        # Status Display
        self.status_text = ctk.CTkTextbox(self, height=100)
        self.status_text.pack(fill="x", padx=20, pady=10)

    ## UI defined, we know need to create commands.     

    def browse_input(self):
        filename = filedialog.askopenfilename(
            filetypes=[("Image files", "*.png *.jpg *.jpeg *.bmp")]
        )
        if filename: #If filename exist, I update the string in the box
            self.input_entry.delete(0, "end") #Remove the old text
            self.input_entry.insert(0, filename)  #Create the new text
            if self.same_output_var.get(): #If the value is 
                self.update_output_path() # Note THAT THE DIRECTORY IS UPDATED ONLY IF WE CHOOSE THE INPUT AFTER CHECKING THE BOX. 
    
    def browse_output(self): #browse the output
        if self.operation_var.get() == "encode":
            filename = filedialog.asksaveasfilename(
                defaultextension=".png",
                filetypes=[("PNG files", "*.png")]
            )
        else:
            filename = filedialog.asksaveasfilename(
                defaultextension=".txt",
                filetypes=[("Text files", "*.txt")]
            )
        if filename: #If there is a path, it changes that. 
            self.output_entry.delete(0, "end")
            self.output_entry.insert(0, filename)
    
    def toggle_output_entry(self):
        if self.same_output_var.get(): 
            self.output_entry.configure(state="disabled")
            self.browse_output_btn.configure(state="disabled")
            self.update_output_path()
        else:
            self.output_entry.configure(state="normal")
            self.browse_output_btn.configure(state="normal")
    
    def update_output_path(self):
        input_path = self.input_entry.get()
        if input_path:
            directory = os.path.dirname(input_path)
            filename = os.path.basename(input_path)
            name, ext = os.path.splitext(filename)
            
            if self.operation_var.get() == "encode":
                new_filename = f"{name}_converted{ext}"
            else:
                new_filename = f"{name}_decoded.txt"
                
            output_path = os.path.join(directory, new_filename)
            self.output_entry.delete(0, "end")
            self.output_entry.insert(0, output_path)
    
    def process_image(self):



        input_path = self.input_entry.get() #check if the input path is inserted
        output_path = self.output_entry.get() #check if the output path is inserted
        message = self.message_text.get("1.0", "end-1c")  #Check the message text
        
        if not input_path:
            messagebox.showerror("Error", "Please select a valid input file")
            return
        
        if not output_path:
            messagebox.showerror("Error", "Please select a valid output location")
            return
        
        try:
            if self.operation_var.get() == "encode":
                if not message:
                    messagebox.showerror("Error", "Please enter a message to encode")
                    return
                
                with Image.open(input_path) as im:
                    encoded = encode_image(im, message)
                    encoded.save(output_path)
                    # Calculate PSNR
                    psnr_value = psnr(im, encoded)
                    
                    self.status_text.delete("1.0", "end")
                    self.status_text.insert("1.0", f"Image encoded successfully!\nPSNR Value: {psnr_value:.2f} dB")
            
            else:  # decode
                with Image.open(input_path) as im:
                    decoded_text = decode_image(im)
                
                # Save decoded text to file
                with open(output_path, 'w') as f:
                    f.write(decoded_text)
                
                self.status_text.delete("1.0", "end")
                self.status_text.insert("1.0", f"Image decoded successfully!\nDecoded text saved to: {output_path}")
        
        except Exception as e:
            self.status_text.delete("1.0", "end")
            self.status_text.insert("1.0", f"Error: {str(e)}")
            messagebox.showerror("Error", str(e))
    

if __name__ == "__main__":
    app = SteganographyGUI()
    app.mainloop()