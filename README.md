# High-Speed PNG to Lossless JXL Converter (With Stable Diffusion Metadata Preservation)

A highly optimized Python tool designed to batch-convert image archives from PNG to JPEG XL (.jxl). 

Unlike standard image compressors that strip away AI data, this tool safely extracts the raw generation text chunk (`parameters`) from Stable Diffusion PNGs and maps it to a binary EXIF `UserComment` structure. Your prompts, seeds, samplers, and generation steps remain **100% readable** by the WebUI's PNG Info tab.

## ✨ Features
* **100% Lossless Compression:** Drastically cuts down file sizes without losing a single pixel of your artwork.
* **Blazing Fast Multiprocessing:** Spins up concurrent tasks to utilize all available CPU threads.
* **Pixel-Perfect Safety Guard:** Automatically runs an internal bit-by-bit image comparison before deleting any original PNGs.
* **Universal Execution:** Runs via your system Python, allowing it to function anywhere on your computer without being locked into a specific Stable Diffusion directory.

## 📦 How to Setup & Run

### 1. Install Prerequisites
This tool uses standard system Python. Open Windows PowerShell or Command Prompt and run the following command to install the required image and metadata libraries globally:

```bash
pip install piexif pillow pillow-jxl

Credits & Acknowledgments
Architectural framework, optimization logic, and multiprocessing layout written with the help of Gemini (Google AI).