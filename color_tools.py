from PIL import Image
#import math
import json

class Color:
    def __init__(self, name="NotGiven", rgb=(0,0,0), label="NotGiven"):
        self._name = name
        self._rgb = tuple(rgb)
        self._label = label

    @property
    def name(self):
        return self._name

    @property
    def rgb(self):
        return self._rgb

    @property
    def label(self):
        return self._label

    def __str__(self):
        return f"{self.name}, RGB {self.rgb}, label {self.label}"
    
def get_colors(file_path):
    colors_dict = {}
    with open(file_path, "r") as file:
        d = json.load(file)
        for color in d["colors"]:
            c = Color(color["name"], color["rgb"], color["label"])
            colors_dict[color["name"]] = c
    return colors_dict    


def distance(color1, color2): #3D distance without the square root (I don't think we need it since it is a increasing function)
    r1, g1, b1 = color1.rgb
    r2, g2, b2 = color2.rgb
    return ((r1 - r2) ** 2 + (g1 - g2) ** 2 + (b1 - b2) ** 2)


def find_closest_color(target_color, palette):
    closest_color = Color("Black", [0,0,0], "B") #I put the first one as default
    min_distance = 195075 #maximum possible distance in RGB space (255^2 + 255^2 + 255^2)

    for color in palette:
        dist = distance(target_color, color)
        if dist < min_distance:
            min_distance = dist
            closest_color = color

    return closest_color


def find_the_average_color(image):
    pixels = list(image.getdata()) #this .getdata() returns a list of RGB pixels
    num_pixels = len(pixels)

    total_r = sum([pixel[0] for pixel in pixels])
    total_g = sum([pixel[1] for pixel in pixels])
    total_b = sum([pixel[2] for pixel in pixels])

    avg_r = total_r // num_pixels
    avg_g = total_g // num_pixels
    avg_b = total_b // num_pixels

    return Color("Average Color", [avg_r, avg_g, avg_b])
