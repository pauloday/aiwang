import sys
import math
from PIL import Image

# rate is how much opacity to add/remove with each distance
def calculate_opacities(distance, num_images, rate = 0.1):
    def calculate_opacity(image_num):
        # ratio of distance to size is percent through cycle
        # cycle 0 is images[0] * 1 -> images[1] * 1, images[0] * 0
        cycle = int(distance / (size / num_images)) % num_images
        next_image = (image_num + 1) % num_images
        opacity = distance / size
        if cycle == image_num:
            return opacity
        elif cycle == next_image:
            return 1 - opacity
        return 0
    return [calculate_opacity(i) for i in range(num_images)]

def blend_pixel(opacities, pixels):
    blended_pixel = [0, 0, 0]
    for opacity, pixel in zip(opacities, pixels):
        for j in range(3):
            blended_pixel[j] += int(pixel[j] * opacity)
    return tuple(blended_pixel)

def combine_images(images, point):
    # Open the input images
    input_images = [Image.open(image) for image in images]

    # Ensure all images have the same size
    width, height = input_images[0].size
    input_images = [img.resize((width, height)) for img in input_images]

    # Create a new image for the combined result
    combined = Image.new('RGB', (width, height))

    # Iterate over each pixel in the images
    for x in range(width):
        for y in range(height):
            distance = math.dist((x, y), point)
            opacities = calculate_opacities(distance, len(images))
            pixels = [img.getpixel((x, y)) for img in input_images]
            blended_pixel = blend_pixel(opacities, pixels)
            combined.putpixel((x, y), blended_pixel)

    # Save the combined image
    combined.save('combined_image.png')

if __name__ == '__main__':
    # Check if the correct number of command-line arguments is provided
    if len(sys.argv) < 5:
        print("Usage: python script.py <image1> <image2> [<image3> ...] <x> <y>")
        sys.exit(1)

    # Extract the image paths from the command-line arguments
    image_paths = sys.argv[1:-2]

    # Extract the point arguments from the command line
    point = (int(sys.argv[-2]), int(sys.argv[-1]))

    # Combine the images
    combine_images(image_paths, point)
