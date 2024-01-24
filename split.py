import sys
import cv2
import shutil
import math
import numpy as np

def apply_transparency(image, index):
# Check if the image has an alpha channel
    if image.shape[2] == 3:
        # Add an alpha channel to the image
        image = cv2.cvtColor(image, cv2.COLOR_BGR2BGRA)

    # Get the dimensions of the image
    height, width, channels = image.shape

    # Create a new transparent image of the same size
    transparent_image = np.zeros((height, width, channels), dtype=np.uint8)

    # Calculate the split point based on the index
    split_point = int(width / 2) if index in [0, 2] else int(height / 2)

    # Set transparency based on the specified index
    if index == 0:  # Top half visible
        transparent_image[:split_point, :] = image[:split_point, :]
    elif index == 1:  # Right half visible
        transparent_image[:, split_point:] = image[:, split_point:]
    elif index == 2:  # Bottom half visible
        transparent_image[split_point:, :] = image[split_point:, :]
    elif index == 3:  # Left half visible
        transparent_image[:, :split_point] = image[:, :split_point]

    # Return the transparent image
    return transparent_image

def fade_image(image, dir):
    # Convert the image to RGBA if it doesn't have an alpha channel
    if image.shape[2] == 3:
        image = cv2.cvtColor(image, cv2.COLOR_BGR2BGRA)

    # Get the width and height of the image
    height, width, channels = image.shape

    # Create a new transparent image of the same size
    fade_image = np.zeros((height, width, channels), dtype=np.uint8)

    # Create the alpha channel for the fade image
    alpha = np.zeros((height, width), dtype=np.uint8)

    # Calculate the transparency based on the x position
    if dir == 0:
        for x in range(width):
            alpha[:, x] = int((1 - abs(x / (width // 2) - 1)) * 255)
    else:
        for y in range(height):
            alpha[:, y] = int((1 - abs(y / (height // 2) - 1)) * 255)

    # Set the alpha channel in the fade image
    fade_image[:, :, 3] = alpha

    # Copy the RGB channels from the original image to the fade image
    fade_image[:, :, :3] = image[:, :, :3]

    # Return the fade image
    return fade_image

def make_faded_quarters(image):
    return [apply_transparency(fade_image(image, i % 2), i) for i in range(4)]

def get_quarter_vertices(image):
    # Get the image dimensions
    height, width = image.shape[:2]
    hheight, hwidth = (height // 2, width // 2)
    theight, twidth = (height // 3, width // 3)
    qheight, qwidth = (height // 4, width // 4)

    # Define the triangle vertices for the quarters
    pts_top = np.array([[0, 0], [width, 0], [hwidth, hheight]], np.int32)
    pts_left = np.array([[0, 0], [hwidth, hheight], [0, height]], np.int32)
    pts_bottom = np.array([[0, height], [width, height], [hwidth, hheight]], np.int32)
    pts_right = np.array([[width, 0], [hwidth, hheight], [width, height]], np.int32)

    return [pts_top, pts_left, pts_bottom, pts_right]


def apply_mask(image, vertices):
    # Create an empty mask
    mask = np.zeros(image.shape[:2], dtype=np.uint8)

    # Fill the triangle mask
    cv2.fillPoly(mask, vertices, 255)

    # Create a copy of the image with transparency
    masked_image = cv2.cvtColor(image, cv2.COLOR_BGR2BGRA)
    masked_image[mask == 0, 3] = 0

    return masked_image


def cut_image_into_quarters(image):
    # Get the quarter vertices
    vertices = get_quarter_vertices(image)

    # Apply the mask to extract each quarter
    quarters = [apply_mask(image, [vertices[i]]) for i in range(4)]

    return quarters


def combine_quarters_by_indices(quarter_indices, quarter_arrays):
    combined_image = np.zeros_like(quarter_arrays[0][0])

    for i in range(4):
        quarter_index = quarter_indices[i]
        quarter_array = quarter_arrays[quarter_index]
        quarter = quarter_array[i]
        combined_image[np.where(quarter[:, :, 3] > 0)] = quarter[np.where(quarter[:, :, 3] > 0)]

    return combined_image


def write_image_to_file(image, filename):
    cv2.imwrite(filename, image)


def generate_all_combinations(n):
    combinations = []

    for i in range(n):
        for j in range(n):
            for k in range(n):
                for l in range(n):
                    combinations.append([i, j, k, l])

    return combinations

if __name__ == "__main__":
    quarters = []
    images = sys.argv[1:]
    for image_path in images:
        image = cv2.imread(image_path)
        #quarters.append(make_faded_quarters(image))
        quarters.append(cut_image_into_quarters(image))

    combinations = generate_all_combinations(len(images))

    for i, combination in enumerate(combinations):
        combined_image = combine_quarters_by_indices(combination, quarters)
        name = "".join(str(c) for c in combination)
        cv2.imwrite(f"./output/{name}.png", combined_image)
        shutil.copy2('./white_box.png', f"./output/masks/{name}.png")
