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
   git clone [https://github.com/daniel-kaliski/PyPhoto.git](https://github.com/daniel-kaliski/PyPhoto.git)
   cd PyPhoto

