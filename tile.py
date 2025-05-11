import argparse
import os
from PIL import Image
from pathlib import Path
from typing import Tuple

def tile_image(image_path: Path, output_dir: Path, tile_dim: Tuple[int, int], overwrite: bool = False) -> None:
    """
    Tiles a single image into smaller pieces.

    Args:
        image_path: Path to the input image.
        output_dir: Directory to save the tiled images.
        tile_dim: A tuple (rows, cols) specifying the tiling dimensions (e.g., (2, 2) for 2x2 tiles).
        overwrite: If True, overwrite existing tiled images.
    """
    try:
        img = Image.open(image_path)
        img_width, img_height = img.size
        tile_width = img_width // tile_dim[1]
        tile_height = img_height // tile_dim[0]

        base_filename = image_path.stem
        file_extension = image_path.suffix

        for i in range(tile_dim[0]):  # Rows
            for j in range(tile_dim[1]):  # Columns
                left = j * tile_width
                upper = i * tile_height
                right = left + tile_width
                lower = upper + tile_height

                tile = img.crop((left, upper, right, lower))
                
                tile_filename = f"{base_filename}_tile_{i}_{j}{file_extension}"
                output_path = output_dir / tile_filename

                if not overwrite and output_path.exists():
                    print(f"Skipping {output_path}, already exists.")
                    continue
                
                tile.save(output_path)
        print(f"Successfully tiled {image_path} into {tile_dim[0]}x{tile_dim[1]} tiles in {output_dir}")

    except FileNotFoundError:
        print(f"Error: Image not found at {image_path}")
    except Exception as e:
        print(f"An error occurred while processing {image_path}: {e}")

def process_directory(input_dir: Path, output_dir: Path, tile_dim: Tuple[int, int], overwrite: bool = False) -> None:
    """
    Processes all images in a directory and tiles them.

    Args:
        input_dir: Directory containing images to tile.
        output_dir: Directory to save the tiled images.
        tile_dim: A tuple (rows, cols) specifying the tiling dimensions.
        overwrite: If True, overwrite existing tiled images.
    """
    if not input_dir.is_dir():
        print(f"Error: Input directory {input_dir} not found or is not a directory.")
        return

    output_dir.mkdir(parents=True, exist_ok=True) # Ensure output directory exists

    supported_formats = ('.png', '.jpg', '.jpeg', '.bmp', '.gif', '.tiff')
    for item in input_dir.iterdir():
        if item.is_file() and item.suffix.lower() in supported_formats:
            tile_image(item, output_dir, tile_dim, overwrite)
        elif item.is_dir():
            print(f"Skipping subdirectory {item}, only processing files in the top-level directory.")


def main():
    """Main function to parse arguments and initiate tiling."""
    parser = argparse.ArgumentParser(
        description="Tile images for machine learning tasks. "
                    "Splits images into a grid of smaller tiles (e.g., 2x2, 3x3)."
    )
    parser.add_argument(
        "input_path",
        type=Path,
        help="Path to the input image file or directory containing images."
    )
    parser.add_argument(
        "-o", "--output_dir",
        type=Path,
        default=Path("./tiled_images"),
        help="Directory to save the tiled images. Defaults to './tiled_images'."
    )
    parser.add_argument(
        "-d", "--dimensions",
        type=str,
        default="2x2",
        help="Tiling dimensions as 'rowsXcols' (e.g., '2x2', '3x4'). Defaults to '2x2'."
    )
    parser.add_argument(
        "--overwrite",
        action="store_true",
        help="Overwrite existing tiled images in the output directory."
    )

    args = parser.parse_args()

    try:
        rows, cols = map(int, args.dimensions.lower().split('x'))
        if rows <= 0 or cols <= 0:
            raise ValueError("Tile dimensions must be positive integers.")
        tile_dim = (rows, cols)
    except ValueError as e:
        print(f"Error: Invalid dimensions format '{args.dimensions}'. Please use 'rowsXcols' (e.g., '2x2'). {e}")
        return

    args.output_dir.mkdir(parents=True, exist_ok=True)

    if args.input_path.is_file():
        print(f"Processing single image: {args.input_path}")
        tile_image(args.input_path, args.output_dir, tile_dim, args.overwrite)
    elif args.input_path.is_dir():
        print(f"Processing directory: {args.input_path}")
        process_directory(args.input_path, args.output_dir, tile_dim, args.overwrite)
    else:
        print(f"Error: Input path {args.input_path} is not a valid file or directory.")

if __name__ == "__main__":
    main()
