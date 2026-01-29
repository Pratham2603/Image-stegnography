import PIL
from PIL import Image, ImageTk # Add ImageTk for Tkinter image display
import numpy as np
import os
from tkinter import *
from tkinter import filedialog, messagebox # To open file dialogs and show alerts

# --- Keep your existing functions here: decode_message_from_pixels, encode_message_into_pixels ---
# Note: You'll need to pass the original image object (for size/mode) and pixel_data to the GUI class.

# Decoding function (Your original code, unchanged for core logic)
def decode_message_from_pixels(pixel_data):
    # ... [Your original decode_message_from_pixels function code] ...
    extracted_binary = []
    i = 0
    while i < len(pixel_data):
        binary_string = ''
        for j in range(8):
            k = i * 9 + j
            if k < len(pixel_data):
                if pixel_data[k] % 2 == 0:
                    binary_string += '0'
                else:
                    binary_string += '1'
        extracted_binary.append(binary_string)

        # Check the last value of every third pixel
        k=i*9+8
        if k < len(pixel_data) and pixel_data[k] % 2 == 1:
            break
        i += 1
    
    extracted_message = ''
    for binary_value in extracted_binary:
        try:
            ascii_char = chr(int(binary_value, 2))
            extracted_message += ascii_char
        except ValueError:
            # Handle cases where binary_value might be incomplete or empty
            pass 

    return extracted_message.strip('\x00') # Remove potential null termination characters

# Encoding function (Your original code, unchanged for core logic)
def encode_message_into_pixels(message, pixel_data):
    # ... [Your original encode_message_into_pixels function code] ...
    Ascii = [ord(char) for char in message]
    Binary = [bin(ascii_value)[2:].zfill(8) for ascii_value in Ascii]
    
    # Add a termination character to the message (e.g., null character \x00) and its binary
    # The original logic uses the 9th pixel as a stop flag, so we'll just encode the message as is.
    
    for i in range(len(Binary)):
        for j in range(8):  # Each binary number is 8 bits
            k = i * 9 + j  # Correctly calculate the index in pixel_data

            if k >= len(pixel_data):
                raise ValueError("Not enough pixel data to encode the entire message.")
            
            # Ensure we don't exceed the length of pixel_data
            if (Binary[i][j] == '0'and pixel_data[k] %2 !=0):
                pixel_data[k]-=1
            elif (Binary[i][j]== '1' and pixel_data[k]%2 == 0):
                if( pixel_data[k]!=0):
                    pixel_data[k]-=1
                else:
                    pixel_data[k]+=1

    # Mark the end of the encoded message
    for z in range(1,len(Binary)+1):
        x=z*9-1
        if x >= len(pixel_data): # Safety check
            break
        
        if(z<len(Binary)):
            if(pixel_data[x]%2==1):
                pixel_data[x]-=1
        elif ((z == len(Binary))):
            if(pixel_data[x]%2== 0):
                if (pixel_data[x]!=0):
                    pixel_data[x]-=1
                else:
                    pixel_data[x]+=1
                    
    return pixel_data


# --- GUI Class Implementation ---

class SteganographyApp:
    def __init__(self, master):
        self.master = master
        master.title("Image Steganography (LSB)")
        master.geometry("700x500")
        master.config(bg='#e3f4f1')

        # Variables to store image data and Tkinter-compatible image object
        self.original_image = None
        self.image_display = None
        self.image_path = ""
        
        # Current active frame
        self.current_frame = None

        # Start with the main menu
        self.create_main_menu()

    def clear_frame(self):
        """Destroys the current frame and resets it."""
        if self.current_frame:
            self.current_frame.destroy()
        
    def create_main_menu(self):
        """Sets up the initial screen with Encode/Decode buttons."""
        self.clear_frame()
        
        self.current_frame = Frame(self.master, bg='#e3f4f1', padx=20, pady=20)
        self.current_frame.pack(fill='both', expand=True)

        Label(self.current_frame, text="Select Operation", font=('Helvetica', 20, 'bold'), bg='#e3f4f1').pack(pady=50)

        Button(self.current_frame, text="🖼 Encode Message", command=self.create_encode_frame, 
               font=('Helvetica', 14), width=20, height=2, bg='#4CAF50', fg='white').pack(pady=15)
        
        Button(self.current_frame, text="🔑 Decode Message", command=self.create_decode_frame, 
               font=('Helvetica', 14), width=20, height=2, bg='#2196F3', fg='white').pack(pady=15)
        
        
    # --- Encoding Functions ---

    def create_encode_frame(self):
        """Sets up the Encoding GUI."""
        self.clear_frame()
        self.current_frame = Frame(self.master, bg='#e3f4f1', padx=10, pady=10)
        self.current_frame.pack(fill='both', expand=True)

        # 1. Image Selection and Display
        img_frame = Frame(self.current_frame, bg='lightgray', width=300, height=300)
        img_frame.grid(row=0, column=0, rowspan=3, padx=10, pady=10, sticky="nsew")
        img_frame.grid_propagate(False) # Prevent frame from shrinking to contents

        self.image_display_label = Label(img_frame, text="No Image Selected", bg='lightgray')
        self.image_display_label.pack(expand=True)
        
        Button(self.current_frame, text="Select Image (PNG/BMP)", command=self.load_image_for_encode, 
               font=('Helvetica', 10), bg='#FF9800').grid(row=3, column=0, pady=5)
        
        # 2. Message Input and Controls
        controls_frame = Frame(self.current_frame, bg='#f0f0f0', padx=10, pady=10)
        controls_frame.grid(row=0, column=1, rowspan=4, padx=10, pady=10, sticky="nsew")
        
        Label(controls_frame, text="Secret Message:", font=('Helvetica', 12, 'bold'), bg='#f0f0f0').pack(pady=5)
        
        self.message_input = Text(controls_frame, height=10, width=40, font=('Helvetica', 10))
        self.message_input.pack(pady=5)
        
        Button(controls_frame, text="🚀 Encode & Save Image", command=self.perform_encode, 
               font=('Helvetica', 12, 'bold'), bg='#4CAF50', fg='white').pack(pady=15, fill='x')
        
        # Status Label
        self.encode_status_label = Label(controls_frame, text="", bg='#f0f0f0', fg='red')
        self.encode_status_label.pack(pady=5)
        
        # Back Button
        Button(self.current_frame, text="⬅ Back to Menu", command=self.create_main_menu, 
               font=('Helvetica', 10), bg='#f44336', fg='white').grid(row=4, column=0, columnspan=2, pady=10)
        
        self.current_frame.grid_columnconfigure(1, weight=1)

    def load_image_for_encode(self):
        """Opens a file dialog and loads the selected image for encoding."""
        self.image_path = filedialog.askopenfilename(
            title="Select Cover Image",
            filetypes=(("PNG files", "*.png"), ("BMP files", "*.bmp"), ("All files", "*.*"))
        )
        if self.image_path:
            try:
                # Force PIL to fully load the image to catch IO errors early
                from PIL import ImageFile, Image
                ImageFile.LOAD_TRUNCATED_IMAGES = True

                img = Image.open(self.image_path)
                img.load()

                # Normalize mode to a predictable number of channels to avoid reshape errors later
                if img.mode not in ('RGB', 'RGBA', 'L'):
                    # convert to RGBA to preserve possible alpha channel
                    img = img.convert('RGBA')

                self.original_image = img

                # Resize image for display purposes
                display_img = self.original_image.copy()
                display_img.thumbnail((280, 280)) # Maintain aspect ratio

                self.image_display = ImageTk.PhotoImage(display_img)
                self.image_display_label.config(image=self.image_display, text="")
                self.encode_status_label.config(text=f"Image loaded: {os.path.basename(self.image_path)}", fg='green')
                
            except Exception as e:
                # Print traceback to console for debugging and show message in UI
                import traceback
                traceback.print_exc()
                messagebox.showerror("Error", f"Failed to load image: {e}")
                self.original_image = None
                self.image_display_label.config(image='', text="Error loading image")
                # Update status label if present
                try:
                    self.encode_status_label.config(text=f"Load error: {e}", fg='red')
                except Exception:
                    pass
                
    def perform_encode(self):
        """Performs the encoding and saves the new image."""
        if not self.original_image:
            messagebox.showerror("Error", "Please select an image first.")
            return

        message = self.message_input.get("1.0", END).strip()
        if not message:
            messagebox.showerror("Error", "Please enter a message to encode.")
            return

        pixel_data = np.array(self.original_image).flatten().tolist()
        
        # Check if the message is too long (8 bits per char + 1 bit for stop flag per char block)
        required_pixels = len(message) * 9
        if len(pixel_data) < required_pixels:
            messagebox.showerror("Error", f"Message is too long. Max chars: {len(pixel_data)//9}")
            return
            
        try:
            self.encode_status_label.config(text="Encoding message...", fg='orange')
            
            # 1. Encode the message
            encoded_pixels = encode_message_into_pixels(message, pixel_data)

            # 2. Reshape the encoded pixel data back to the original image dimensions
            # Use the original image's size and mode to correctly reshape
            w, h = self.original_image.size
            if self.original_image.mode == 'L': # Grayscale
                channels = 1
            elif self.original_image.mode in ('RGB', 'RGBA'):
                channels = len(self.original_image.getbands())
            else:
                channels = -1 # Let numpy infer the shape
            
            # Reshape based on original dimensions
            new_image_array = np.array(encoded_pixels, dtype=np.uint8).reshape(h, w, channels)
            
            # 3. Save the new image
            # Use PIL.Image.fromarray via the PIL package reference to avoid name shadowing
            new_image = PIL.Image.fromarray(new_image_array, self.original_image.mode)
            
            save_path = filedialog.asksaveasfilename(
                defaultextension=".png", 
                filetypes=[("PNG files", "*.png")],
                title="Save Encoded Image As"
            )
            
            if save_path:
                new_image.save(save_path)
                self.encode_status_label.config(text=f"Success! Saved as {os.path.basename(save_path)}", fg='green')
            else:
                self.encode_status_label.config(text="Save cancelled.", fg='red')
                
        except Exception as e:
            messagebox.showerror("Encoding Error", f"An error occurred during encoding: {e}")
            self.encode_status_label.config(text="Encoding failed.", fg='red')


    # --- Decoding Functions ---

    def create_decode_frame(self):
        """Sets up the Decoding GUI."""
        self.clear_frame()
        self.current_frame = Frame(self.master, bg='#e3f4f1', padx=10, pady=10)
        self.current_frame.pack(fill='both', expand=True)

        # 1. Image Selection and Display
        img_frame = Frame(self.current_frame, bg='lightgray', width=300, height=300)
        img_frame.grid(row=0, column=0, rowspan=3, padx=10, pady=10, sticky="nsew")
        img_frame.grid_propagate(False)

        self.decode_image_display_label = Label(img_frame, text="No Encoded Image Selected", bg='lightgray')
        self.decode_image_display_label.pack(expand=True)
        
        Button(self.current_frame, text="Select Encoded Image", command=self.load_image_for_decode, 
               font=('Helvetica', 10), bg='#FF9800').grid(row=3, column=0, pady=5)
        
        # 2. Output and Controls
        controls_frame = Frame(self.current_frame, bg='#f0f0f0', padx=10, pady=10)
        controls_frame.grid(row=0, column=1, rowspan=4, padx=10, pady=10, sticky="nsew")
        
        Button(controls_frame, text="🔑 Decode Message", command=self.perform_decode, 
               font=('Helvetica', 12, 'bold'), bg='#2196F3', fg='white').pack(pady=15, fill='x')

        Label(controls_frame, text="Extracted Message:", font=('Helvetica', 12, 'bold'), bg='#f0f0f0').pack(pady=5)
        
        self.message_output = Text(controls_frame, height=10, width=40, font=('Helvetica', 10), state=DISABLED)
        self.message_output.pack(pady=5)
        
        # Status Label
        self.decode_status_label = Label(controls_frame, text="", bg='#f0f0f0', fg='red')
        self.decode_status_label.pack(pady=5)
        
        # Back Button
        Button(self.current_frame, text="⬅ Back to Menu", command=self.create_main_menu, 
               font=('Helvetica', 10), bg='#f44336', fg='white').grid(row=4, column=0, columnspan=2, pady=10)
        
        self.current_frame.grid_columnconfigure(1, weight=1)

    def load_image_for_decode(self):
        """Loads an image for decoding."""
        self.image_path = filedialog.askopenfilename(
            title="Select Encoded Image",
            filetypes=(("PNG files", "*.png"), ("BMP files", "*.bmp"), ("All files", "*.*"))
        )
        if self.image_path:
            try:
                from PIL import ImageFile, Image
                ImageFile.LOAD_TRUNCATED_IMAGES = True

                img = Image.open(self.image_path)
                img.load()

                if img.mode not in ('RGB', 'RGBA', 'L'):
                    img = img.convert('RGBA')

                self.original_image = img

                # Resize image for display purposes
                display_img = self.original_image.copy()
                display_img.thumbnail((280, 280)) 

                self.image_display = ImageTk.PhotoImage(display_img)
                self.decode_image_display_label.config(image=self.image_display, text="")
                self.decode_status_label.config(text=f"Image loaded: {os.path.basename(self.image_path)}", fg='green')
                self.clear_output()
                
            except Exception as e:
                import traceback
                traceback.print_exc()
                messagebox.showerror("Error", f"Failed to load image: {e}")
                self.original_image = None
                self.decode_image_display_label.config(image='', text="Error loading image")
                try:
                    self.decode_status_label.config(text=f"Load error: {e}", fg='red')
                except Exception:
                    pass

    def clear_output(self):
        self.message_output.config(state=NORMAL)
        self.message_output.delete("1.0", END)
        self.message_output.config(state=DISABLED)

    def perform_decode(self):
        """Performs the decoding and displays the message."""
        if not self.original_image:
            messagebox.showerror("Error", "Please select an image to decode.")
            return
            
        try:
            self.decode_status_label.config(text="Decoding message...", fg='orange')
            self.clear_output()
            
            pixel_data = np.array(self.original_image).flatten().tolist()
            
            # Call your core decoding function
            decoded_message = decode_message_from_pixels(pixel_data)
            
            if decoded_message:
                self.message_output.config(state=NORMAL)
                self.message_output.insert(END, decoded_message)
                self.message_output.config(state=DISABLED)
                self.decode_status_label.config(text="Success! Message extracted.", fg='green')
            else:
                self.decode_status_label.config(text="Could not find a hidden message.", fg='red')
            
        except Exception as e:
            messagebox.showerror("Decoding Error", f"An error occurred during decoding: {e}")
            self.decode_status_label.config(text="Decoding failed.", fg='red')


# --- Main Execution Block ---
if __name__ == '__main__':
    try:
        root = Tk()
        app = SteganographyApp(root)
        root.mainloop()
    except Exception as e:
        import traceback
        traceback.print_exc()
        messagebox.showerror("Startup Error", f"An error occurred starting the application:\n{e}")