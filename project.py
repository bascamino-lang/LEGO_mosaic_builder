
import sys
import os
from color_tools import Color, find_closest_color, find_the_average_color, get_colors
from PIL import Image
from bricks_costants import brick_length, brick_height, brick_face_ration
from mosaic_builder import build_plain_mosaic, build_mosaic, draw_mosaic, Brick
from outputs import mosaic_instruction, mosaic_components


        
def main():
    try:
        base_dir = os.path.dirname(__file__)  # cartella in cui si trova project.pyi
        #json_path = os.path.join(base_dir, "colorsWithoutGray.json")
        #json_path = os.path.join(base_dir, "colorsWithoutLav.json")
        json_path = os.path.join(base_dir, "colors.json")
        #json_path = os.path.join(base_dir, "colorsForIcarus.json")
        #json_path = os.path.join(base_dir, "colorsForT.json")
        colors_dict = get_colors(json_path)

    except FileNotFoundError:
            print("Problem in the colors dictionary file path.")
            sys.exit(1)

    while True:
        try:
            file_path = input("Enter the image file path: (images/example1.jpg) ")
            image = Image.open(file_path) #open the file once
            break

        except FileNotFoundError:
            print("The specified image file was not found.")
    
    while True:
        output_path = input("Enter the output file path for the mosaic image (PLS, specificy the extension): ")

        if not output_path.endswith(('.png', '.jpg', '.jpeg', '.bmp')):
            print("Please provide a valid image file extension for the output path (e.g., .png, .jpg, .jpeg, .bmp).")
        
        else:
            break

    while True:
        m = input("Enter the desired mosaic length in cm: ").strip()

        if m.endswith("cm"):
            m = m[:-2].strip()

        m = float(m.strip())

        if m < brick_length or m <= 0:
            print(f"Invalid size of the mosaic. The minimum mosaic length is {brick_length} cm.")
        else:
            break

    m = int(m)

    sizes = build_plain_mosaic(image, m)

    mosaic = build_mosaic(image, sizes[0][0], sizes[0][1], colors_dict)

    draw_mosaic(mosaic, output_path, sizes[1][0], sizes[1][1])

    remove_end = output_path.split(".")[0] #I remove the extension .jpeg or similar
    output_path = remove_end + ".txt"

    mosaic_instruction(mosaic, output_path)
    mosaic_components(mosaic, output_path)

if __name__ == "__main__":
    main()