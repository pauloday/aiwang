import cv2
import numpy as np

def fade_image(image_path):
    # Read the image using OpenCV
    image = cv2.imread(image_path, cv2.IMREAD_UNCHANGED)

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
    for x in range(width):
        alpha[:, x] = int((1 - abs(x / (width // 2) - 1)) * 255)
        print(alpha)

    # Set the alpha channel in the fade image
    fade_image[:, :, 3] = alpha

    # Copy the RGB channels from the original image to the fade image
    fade_image[:, :, :3] = image[:, :, :3]

    # Return the fade image
    return fade_image

# Example usage
faded_image = fade_image('fish.png')
cv2.imwrite('faded_image.png', faded_image)
