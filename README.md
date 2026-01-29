# Image Steganography GUI (stego gui2.py)

A lightweight Tkinter application that implements simple least-significant-bit (LSB) image steganography. The GUI lets you encode a short secret message into a PNG/BMP image and decode a hidden message from an image produced by this app.

## Features

- Select an image (PNG/BMP or others) and embed a secret text message into the image's pixel data using per-channel LSB changes.
- Decode and extract the hidden message from an image created by this tool.
- Small, user-friendly Tkinter interface with simple status messages and error dialogs.

## Files

- `stego gui2.py` — Main application. Implements the GUI, encode/decode logic, and image IO.

## Requirements

- Python 3.8+
- Pillow (PIL)
- numpy

Install dependencies with pip:

```powershell
python -m pip install --upgrade pip
python -m pip install pillow numpy
```

## How to run

Open a PowerShell terminal and run:

```powershell
python "d:\Python Gui\stego gui2.py"
```

The window should appear. Use "Select Image" to choose a cover image (PNG or BMP recommended), enter a secret message, and click "Encode & Save Image" to write a new file.

To decode, choose the encoded image using "Select Encoded Image" and click "Decode Message".

## Notes & Troubleshooting

- If the app shows "Failed to load image", check the console for a printed traceback. Common causes:
  - Incomplete/truncated image files (try re-downloading or opening in an image viewer).
  - Unsupported or unusual image modes. The app converts non-RGB images to RGBA where possible.
  - Permission errors when accessing the file path.

- Encoding capacity: The app currently reserves 9 channel values per character (8 bits + 1 stop/flag bit). That means the maximum storable characters is approximately floor((width × height × channels) / 9).

- Unicode: If you need full UTF-8 support for non-ASCII characters, consider updating the encode/decode logic to operate on the message's UTF-8 bytes instead of Python code points.

- If you see an error like "no attribute named fromarray", ensure Pillow is installed and up-to-date. The app uses `PIL.Image.fromarray` internally to construct the encoded image; explicit `import PIL` is used to avoid name shadowing.

## Recommended improvements (optional)

- Replace the per-character stop flag with a header that stores message length (more efficient use of capacity).
- Support encoding arbitrary binary payloads (files) instead of just text.
- Add unit tests that encode/decode a short message on a generated image and assert round-trip equality.

## License

This project is provided as-is for educational purposes. No license included.
