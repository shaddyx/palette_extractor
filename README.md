# Palette extractor

 Extracts a color palette from an image and saves it to a file

## Installation

```bash
    cd src
    pip install -r requirements.txt
```


## Usage

```bash
  python main.py image.png --colors 32
```

## Arguments

- `image.png`: The path to the input image file.
- `--colors N`: The number of colors to extract from the image. Default is 32.

The output will be a PNG file using pattern `{original_filename}_palette.png` with a color palette of the specified number of colors.


