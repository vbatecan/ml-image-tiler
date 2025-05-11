# Image Tiler for Machine Learning

This script tiles images into smaller pieces, which can be useful for machine learning tasks where focusing on smaller details within an image is beneficial.

## Description

The script can process a single image file or all supported image files within a specified directory. It splits each image into a grid of tiles based on user-defined dimensions (e.g., 2x2, 3x3).

Supported image formats: PNG, JPG/JPEG, BMP, GIF, TIFF.

## Setup and Installation

1.  **Clone the repository (if applicable) or download the `tile.py` script.**

2.  **Create a virtual environment (recommended):**
    ```bash
    python -m venv venv
    ```

3.  **Activate the virtual environment:**
    *   On Windows:
        ```bash
        .\venv\Scripts\activate
        ```
    *   On macOS and Linux:
        ```bash
        source venv/bin/activate
        ```

4.  **Install the required dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

## Usage

The script is run from the command line.

```bash
python tile.py <input_path> [options]
```

### Arguments:

*   `input_path`: (Required) Path to the input image file or a directory containing images.

### Options:

*   `-o OUTPUT_DIR`, `--output_dir OUTPUT_DIR`:
    Directory to save the tiled images. 
    Defaults to `./tiled_images` in the current working directory.
*   `-d DIMENSIONS`, `--dimensions DIMENSIONS`:
    Tiling dimensions as 'rowsXcols' (e.g., '2x2', '3x4'). 
    Defaults to '2x2'.
*   `--overwrite`:
    If specified, the script will overwrite existing tiled images in the output directory. By default, it skips existing files.
*   `-h`, `--help`:
    Show the help message and exit.

### Examples:

1.  **Tile a single image into 2x2 tiles:**
    ```bash
    python tile.py path/to/your/image.jpg
    ```
    Tiled images will be saved in `./tiled_images/`.

2.  **Tile a single image into 3x3 tiles and specify an output directory:**
    ```bash
    python tile.py path/to/your/image.png -d 3x3 -o path/to/custom_output
    ```

3.  **Tile all images in a directory into 4x2 tiles:**
    ```bash
    python tile.py path/to/your/image_directory/ -d 4x2
    ```
    Tiled images for each source image will be saved in subdirectories within `./tiled_images/` (or the custom output directory).

4.  **Tile images and overwrite existing output files:**
    ```bash
    python tile.py path/to/your/image.jpeg --overwrite
    ```

## How Tiling Works

The script divides the image into a grid of `rows` x `cols`.
For an image of width `W` and height `H`, each tile will have a width of approximately `W / cols` and a height of `H / rows`.

The naming convention for tiled images is `original_filename_tile_row_col.extension` (e.g., `my_image_tile_0_0.jpg`, `my_image_tile_0_1.jpg`, etc.). 