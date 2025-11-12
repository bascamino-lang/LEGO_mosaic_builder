from PIL import Image, ImageDraw
from color_tools import Color, find_closest_color, find_the_average_color, get_colors
from bricks_costants import brick_length, brick_height, brick_face_ration
import math

class Brick:
    def __init__(self, length=1, color=None):
        self._length = length
        self._color = color

    @property
    def length(self):
        return self._length

    @property
    def color(self):
        return self._color

    def __str__(self):
        return f"Brick: 1x{self.length}, Color: {self.color.name if self.color else 'None'}"

    def lengh_in_mm(self):
        return self.length * brick_length

def build_plain_mosaic(image, final_lenght):
    
    pixel_lenght, pixel_height = image.size

    number_of_colomns = math.floor(final_lenght / brick_length)
    number_of_rows = math.floor((number_of_colomns *  brick_length * pixel_height) / (pixel_lenght*brick_height))

    return [[number_of_colomns, number_of_rows],[pixel_lenght/number_of_colomns, pixel_height/number_of_rows]] #this tells me how many bricks I need in each direction and the number of pixels each brick will cover

def build_mosaic(image, number_of_colomns, number_of_rows, colors_dict):
            
    pixel_lenght, pixel_height = image.size

    brick_pixel_lenght = pixel_lenght / number_of_colomns
    brick_pixel_height = pixel_height / number_of_rows

    mosaic_bricks = []

    for row in range(number_of_rows):
        mosaic_row = []

        for col in range(number_of_colomns):
            left = int(col * brick_pixel_lenght)
            upper = int(row * brick_pixel_height)
            right = int((col + 1) * brick_pixel_lenght)
            lower = int((row + 1) * brick_pixel_height)

            brick_area = image.crop((left, upper, right, lower))
            average_color = find_the_average_color(brick_area)
            closest_color = find_closest_color(average_color, colors_dict.values())

            mosaic_row.append(Brick(length=1, color=closest_color))
        mosaic_bricks.append(mosaic_row)

    return mosaic_bricks

def draw_mosaic(mosaic, output_path, brick_pixel_lenght, brick_pixel_height):
    number_of_rows = len(mosaic)
    number_of_colomns = len(mosaic[0])

    if number_of_rows == 0 or number_of_colomns == 0:
        raise ValueError("Mosaic cannot be empty.")

    mosaic_image = Image.new("RGB", (int(number_of_colomns * brick_pixel_lenght), int(number_of_rows * brick_pixel_height)))
    draw = ImageDraw.Draw(mosaic_image)

    for row in range(number_of_rows):
        for col in range(number_of_colomns):
            brick = mosaic[row][col]
            left = int(col * brick_pixel_lenght)
            upper = int(row * brick_pixel_height)
            right = int((col + 1) * brick_pixel_lenght)
            lower = int((row + 1) * brick_pixel_height)

            draw.rectangle([left, upper, right, lower], fill=brick.color.rgb)
    try:
        mosaic_image.save(f"images/{output_path}")
    
    except Exception as e:
        print(f"An error occurred while saving the image: {e}")