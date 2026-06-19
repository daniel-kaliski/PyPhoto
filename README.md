# PyPhoto - Image Editor in Python

PyPhoto is a modern, multi-layer desktop application for image editing, written in Python. It uses the `customtkinter` library to render a modern interface (Dark Mode) and the advanced capabilities of the `Pillow` and `rembg` libraries for image processing and artificial intelligence.

The application offers features known from professional graphic programs, such as layer support, keyboard shortcuts, and intelligent background removal.

## Main Features

* **Multi-layer engine (Layers System):** 
  * Adding empty layers and inserting images from the disk as new layers.
  * Reordering, hiding (visibility), deleting, and renaming layers.
  * Opacity slider for each layer independently.
* **AI Background Removal:** An integrated AI model (`rembg`) that allows you to cut out the background from any layer with a single click.
* **Interactive Tools:**
  * ✋ **Move:** Free positioning of the image on the layer.
  * 🖌 **Brush:** Drawing with adjustable thickness and color.
  * 🔤 **Text:** Inserting text with full font size control.
  * ⬜ **Rectangle:** Drawing geometric shapes.
* **Adjustments and Filters:**
  * Smooth real-time adjustments: Brightness, Contrast, Saturation, Sharpness, and Scale.
  * Ready-made filters: Black & White, Blur, Sharpen, Invert, Emboss, Edge Detection.
* **Global Cropping:** A tool for precise (via mouse or pixel-perfect) cropping of the entire working canvas.
* **Operation History:** A built-in undo system that remembers the last 8 project states.
* **Multilingual:** The application automatically detects the system language or allows manual switching (Polish / English).

## Keyboard Shortcuts (based on industry standards)

Working with PyPhoto is fast and intuitive thanks to built-in shortcuts (they work with the `Ctrl` key on Windows/Linux and `Cmd` on macOS):

* `Ctrl/Cmd + O` - Open project
* `Ctrl/Cmd + S` - Save / Export image
* `Ctrl/Cmd + Z` - Undo

**Tools (single key activation):**
* `V` - Move
* `B` - Brush
* `T` - Text
* `R` - Rectangle
* `C` - Crop

## Requirements and Installation

To run the application locally, make sure you have Python installed (version 3.8+).

1. Clone the repository:

   ```bash
   git clone https://github.com/daniel-kaliski/PyPhoto.git
   cd PyPhoto

2. Install the required libraries:

   ```bash
   pip install customtkinter Pillow rembg

3. Run the application:

   ```bash
   python PyPhoto.py

**Technologies Used**
`CustomTkinter`: A modern, theme-supporting graphical user interface.

`Pillow` (PIL): The main engine for pixel grid processing, Alpha channel manipulation, and image composition.

`rembg`: A machine learning tool for precise background removal.

**Screenshot**

<img width="1500" height="757" alt="1" src="https://github.com/user-attachments/assets/6b0635c7-50f7-423e-bf92-4fe43856f0df" />

<img width="1500" height="757" alt="2" src="https://github.com/user-attachments/assets/d9223a8c-28df-452d-a641-5bc9f81990f4" />

**License**

This project is licensed under the GNU General Public License v3.0 (GPL-3.0). Detailed information can be found in the LICENSE file or at opensource.org/license/gpl-3.0.

Author: Daniel Kaliski
