# Cube Model Generator

[![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)](https://python.org)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Release](https://img.shields.io/github/v/release/Pinguini456/CubeModelFromTexture?include_prereleases)](https://github.com/yourusername/CubeModelFromTexture/releases)

A lightweight desktop application that transforms 2D textures into rendered isometric cube models. Perfect for generating Minecraft-style item icons, block renders, or game assets with proper lighting and perspective.

## Features

- **Single & Bulk Conversion** — Process one texture set or convert entire directories at once
- **Isometric Rendering** — Generates professional 3D cube renders with correct perspective
- **Stair Mode** — Create stair-shaped block models in addition to full cubes
- **Customizable Dimensions** — Control both output image size and cube proportions
- **Smart Lighting** — Automatic shading on faces (left: 83%, right: 68.5%) for depth
- **Drag & Drop Interface** — Simple file browser for selecting textures and output folders

## Download

### Windows Executable

Download the latest release from the [Releases](https://github.com/Pinguini456/CubeModelFromTexture/releases) page. No Python installation required.

1. Download `CubeModelGenerator.exe` from the latest release
2. Run the executable
3. Select your textures and click **Start**

### From Source

```bash
# Clone the repository
git clone https://github.com/yourusername/CubeModelFromTexture.git
cd CubeModelFromTexture

# Install dependencies
pip install -r requirements.txt

# Run the application
python main.py
```

## Usage

### Single Texture Mode

1. **Input Image Size** — Set the resolution of your source textures (e.g., `16x16` for Minecraft textures)
2. **Model Size** — Set the rendered cube dimensions in pixels
3. **Select Textures** — Choose separate images for:
   - **Top texture** — The upper face of the cube
   - **Left texture** — The left-facing side
   - **Right texture** — The right-facing side
4. **Output Folder** — Choose where rendered images will be saved
5. **Optional Settings**:
   - Enable "Use Stair Shape" for stair block renders
   - Disable "Bulk Convert" for single file processing
6. Click **Start** to generate your model

### Bulk Conversion Mode

1. Enable **Bulk Convert** checkbox
2. Select a folder containing multiple textures
3. Each texture will be applied to all three faces of the cube
4. All rendered models are saved to the specified output folder

## Input Requirements

| Parameter | Supported Formats | Notes |
|-----------|-------------------|-------|
| Textures | PNG (with transparency) | RGBA format recommended |
| Image Size | Any resolution | Set to match your texture resolution |
| Model Size | Any positive integer | Output cube dimensions in pixels |

## Building from Source

### Requirements

- Python 3.10 or higher
- Dependencies:
  - `pygame>=2.5.0`
  - `numpy>=1.24.0`
  - `opencv-python>=4.8.0`
  - `Pillow>=10.0.0`



## Project Structure

```
CubeModelFromTexture/
├── main.py          # Application entry point
├── form.py          # Tkinter GUI implementation
├── render.py        # 3D rendering engine (Pygame/OpenCV)
├── temp/            # Temporary processing files
└── requirements.txt # Python dependencies
```

## Technical Details

The rendering pipeline uses:
- **Pygame** — 3D point projection and surface compositing
- **NumPy** — Matrix transformations for rotation and scaling
- **OpenCV** — Perspective warping of textures onto cube faces
- **PIL/Pillow** — Image resizing, rotation, and alpha channel handling

Cube faces are transformed using perspective projection matrices to achieve the classic isometric game asset look.

## License

This project is licensed under the MIT License — see the [LICENSE](LICENSE) file for details.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## Acknowledgments

- Inspired by Minecraft's isometric item rendering
- Built with [Pygame](https://www.pygame.org/) and [OpenCV](https://opencv.org/)

---

**Note:** This is an independent tool and is not affiliated with Mojang Studios or Minecraft.
