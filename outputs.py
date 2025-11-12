
from color_tools import Color
from mosaic_builder import Brick
import os


def mosaic_instruction(mosaic, filename="mosaic.txt"):

    filename = filename if filename.endswith(".txt") else filename + ".txt"

    filename = "instructions_" + filename

    output_dir = "output"
    os.makedirs(output_dir, exist_ok=True)

    output_path = os.path.join(output_dir, filename)

    with open(output_path, "w") as f:
        for row in mosaic:
            # crea una stringa con i label separati da spazi
            line = " ".join(brick.color.label for brick in row)
            f.write(line + "\n")

def mosaic_components(mosaic, filename="mosaic_components.txt"):

    filename = filename if filename.endswith(".txt") else filename + ".txt"
    filename = "components_" + filename

    output_dir = "output"
    os.makedirs(output_dir, exist_ok=True)

    output_path = os.path.join(output_dir, filename)

    components = {}

    for row in mosaic:
        col_idx = 0
        while col_idx < len(row):
            current_label = row[col_idx].color.label
            run_length = 1


            while (
                col_idx + run_length < len(row)
                and row[col_idx + run_length].color.label == current_label 
                and run_length < 4 #max brick length is 4
            ):
                run_length += 1

            if current_label not in components:
                components[current_label] = {1: 0, 2: 0, 3: 0, 4: 0}
            components[current_label][run_length] += 1

            col_idx += run_length

    with open(output_path, "w") as f:
        total_pieces = 0
        for label, sizes in components.items():
            f.write(f"{label}:\n")
            for size in sorted(sizes.keys()):
                count = sizes[size]
                if count > 0:
                    f.write(f"  1x{size}: {count}\n")
                    total_pieces += count
            f.write("\n")
        f.write(f"Total bricks: {total_pieces}\n")
