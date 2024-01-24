from PIL import Image, ImageDraw

def create_gradient_image(width, height, edge_pixels, border_width):
    image = Image.new("RGB", (width, height), (0, 0, 0))  # Create a black image
    draw = ImageDraw.Draw(image)

    gradient_width = width - 2 * edge_pixels
    gradient_height = height - 2 * edge_pixels
    gradient_left = edge_pixels
    gradient_top = edge_pixels
    gradient_right = gradient_left + gradient_width
    gradient_bottom = gradient_top + gradient_height

    center_x, center_y = width // 2, height // 2
    max_distance = max(center_x - gradient_left, center_y - gradient_top)

    for y in range(gradient_top, gradient_bottom):
        for x in range(gradient_left, gradient_right):
            distance_x = abs(x - center_x)
            distance_y = abs(y - center_y)
            distance = max(distance_x, distance_y)

            intensity = int((1 - (distance / max_distance)) * 255)
            color = (intensity, intensity, intensity)

            draw.point((x, y), color)

    # Draw black border
    for i in range(border_width):
        draw.rectangle((i, i, width-i-1, height-i-1), outline=(0, 0, 0))

    return image

def create_white_box_image(width, height):
    image = Image.new("RGB", (width, height), (255, 255, 255))  # Create a black image
    draw = ImageDraw.Draw(image)

    border_width = 32
    box_width = width - 2 * border_width
    box_height = height - 2 * border_width
    box_left = border_width
    box_top = border_width
    box_right = box_left + box_width
    box_bottom = box_top + box_height

    draw.rectangle((box_left, box_top, box_right, box_bottom), fill=(0, 0, 0))

    return image

image_width = 512
image_height = 512
edge_pixel_count = -1000
border_width = 1

# gradient_image = create_gradient_image(image_width, image_height, edge_pixel_count, border_width)
# gradient_image.save("gradient_image.png", "PNG")
# print("Image saved as gradient_image.png")
box_image = create_white_box_image(image_width, image_height)
box_image.save("box.png", "PNG")
