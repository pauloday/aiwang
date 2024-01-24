import os
import re
import random
import time
from PIL import Image, ImageDraw, ImageFont

seed = 68
width = 12
height = 12
size = 512

def add_text_to_image(text, image):
    image_with_text = image.copy()

    draw = ImageDraw.Draw(image_with_text)
    draw.text((10, 10), text, fill='white')

    return image_with_text


def random_tiling(directory, width, height, size):
    tiles = []
    for file in os.listdir(directory):
        print(file)
        file_path = os.path.join(directory, file)
        if not(os.path.isdir(file_path))  :
            tiles.append(file)

    tiling = [[None] * width for _ in range(height)]
    tiling[0][0] = random.choice(tiles)

    for x in range(width):
        for y in range(height):
            regex = ".*"
            for i, (dx, dy) in enumerate([(0, -1), (-1, 0), (0, 1), (1, 0)]):
                nx, ny = x + dx, y + dy
                if ny < 0 or ny >= len(tiling) or nx < 0 or nx >= len(tiling[0]) or tiling[ny][nx] == None:
                        regex += "[0-9]"
                        continue
                tile = tiling[ny][nx]
                regex += tile[(i + 2) % 4]
            regex += ".*.png"
            pattern = re.compile(regex)
            tile_candidates = [tile for tile in tiles if re.match(pattern, tile)]
            tiling[y][x] = random.choice(tile_candidates)
            tiles.remove(tiling[y][x])

    result_width = width * size
    result_height = height * size
    result_image = Image.new('RGB', (result_width, result_height))

    for x in range(width):
        for y in range(height):
            image_path = os.path.join(directory, tiling[y][x])
            if image_path:
                image = Image.open(image_path)
                image = image.resize((size, size))
                # image = add_text_to_image(tiling[y][x], image)
                result_image.paste(image, (x * size, y * size))
    result_image.save(f"./{seed}-{width}-{height}-{time.time()}.png")
                

# Example usage
directory = './output/aiout'

random.seed(seed)
random_tiling(directory, width, height, size)
