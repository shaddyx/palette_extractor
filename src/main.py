import argparse
from typing import List, Tuple

import numpy as np
from PIL import Image, ImageDraw, ImageFont
from sklearn.cluster import KMeans

parser = argparse.ArgumentParser(
    prog='ProgramName',
    description='What the program does',
    epilog='Text at the bottom of help')
parser.add_argument('filename', type=str)
parser.add_argument("--colors", type=int, default=32)
args = parser.parse_args()

output_file = "{}_palette.png".format(args.filename.split(".")[0])
output_txt = "{}_colors.palette".format(args.filename.split(".")[0])


def get_colors(data):
    colors = set([])
    for item in data:
        colors.add(item)
    return colors

# print(colors)
# print(len(colors))


def reduce_colors(data: List[Tuple[int, int, int]], num_colors: int = 16) -> List[Tuple[int, int, int]]:
    """
    Reduces a list of RGB color tuples to a specified number of colors using k-means clustering.

    Args:
        data: A list of RGB color tuples.
        num_colors: The desired number of colors in the reduced list.

    Returns:
        A list of RGB color tuples representing the reduced color palette.
    """

    if not data:
        return []

    # Convert the list of tuples to a NumPy array
    colors = np.array(data)

    # Perform k-means clustering
    kmeans = KMeans(n_clusters=num_colors, n_init=10)  # added n_init to avoid warning
    kmeans.fit(colors)

    # Get the cluster centers (the reduced colors)
    reduced_colors = kmeans.cluster_centers_.astype(int).tolist()

    return [tuple(color) for color in reduced_colors]


def create_color_palette_image(colors: List[Tuple[int, int, int]], square_width: int = 150, square_heigth: int = 50) -> Image.Image:
    """
    Creates an image showing a color palette from a list of RGB color tuples.

    Args:
        colors: A list of 16 RGB color tuples.
        square_heigth: The size (in pixels) of each color square in the image.

    Returns:
        A PIL Image object representing the color palette.
    """

    image_width = square_width * 2
    image_height = square_heigth * len(colors)

    image = Image.new("RGB", (image_width, image_height))
    pixels = image.load()

    for i, color_chunk in enumerate(colors):
        #add hex color to image
        hex_color = "#%02x%02x%02x" % color_chunk
        # draw.text((0, i * square_heigth), hex_color, (0, 0, 0))
        for y in range(i * square_heigth, (i + 1) * square_heigth):
            for x in range(square_width):
                pixels[x, y] = color_chunk

    draw = ImageDraw.Draw(image)
    font = ImageFont.truetype('Pillow/Tests/fonts/FreeMono.ttf', 32)
    for i, color_chunk in enumerate(colors):
        hex_color = "#%02x%02x%02x" % color_chunk
        draw.text((square_width, i * square_heigth), hex_color, (255, 255, 255), font)
    return image


im = Image.open(args.filename)
data = im.getdata()
colors = get_colors(data)
reduced = reduce_colors(list(colors), args.colors)
palette_image = create_color_palette_image(reduced)
palette_image.show()  # to show image
palette_image.save(output_file)  # to save image

# save colors into file in hex
with open(output_txt, "w") as f:
    res = []
    for color in reduced:
        # format tuple to hex
        color = "#%02x%02x%02x" % color
        res.append(color)
    color = ",".join(res)
    f.write(f"{color}\n")
