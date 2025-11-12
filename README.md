# Make a LEGO Mosaic
#### Video Demo:  <www.google.it>
#### Description:
This program takes a picture and produces a lego mosaic from it.
The colors, sizes, and measurements are taken from the **Canadian LEGO website**.
This program has *three* outputs: a picture that shows you how the mosaic will be and two text files saved in the folder *ouuput*.
One of the text files is a list of bricks you need to buy from the LEGO Store
to make the mosaic and the other contains the instructions for building it. 

#### What you need

The program takes the color from a *.json* file. I made one with 12 standard colors, however, sometimes the mosaic looks better if you exclude some of them. You can either use the file *colors.json* or create your own palette.

This project requires the following libraries: *PIL* for image and color management, *os* for file paths, and *math* for basic calculations.

#### The inputs

After running `project.py`, you’ll be asked to provide three input values:

    1) the name of an image you want to make a mosaic from

    2) under which name you want to save the mosaic

    3) the length in cm of the final mosaic


## The files of the projects

The a .json files are color dictionaries. The folder *images* contains all the images and the mosaic. The folder *output* contains the text files. 

### bricks_constants.py
Contains the sizes of the brick 1x1 of LEGO. Since we are going to stack the bricks in the same direction as the logo, we will see only the lateral face of the brick. Moreover, an 1x2 brick is going to be seen as two 1x1 consecuitive bricks merged. Similarly, a 1x3 and 1x4 brick is going to be a three or four consecutive 1x1 bricks merged.

### color_tools.py
This module contains the class `Color` which provides a simple representation of colours using RGB values. Each instance stores an optional name, an RGB tuple (defaulting to (0, 0, 0), i.e. black), and an optional label. The color labels are used in the instructions file and so they should be short, I used labels from magic the gathering. With the RGB tuple, every color can be seen as a vector in the cube [0,255]^3.

The function `get_colors` reads the .json file with the colors and convert into a dictionary (a palette). The function `distance` is the 3D euclidian distance. The function `find_closest_color` takes a color and a palette (dict of colors) and returns the element of the palette that is the closest to the target color. This is done by interpreting a color of a vector in the cube [0,255]^3 and by computing the distances between colors/vectors.
The function `find_the_average_color` takes an image (a file) as an input, via *getdata()* it lists every pixel with the RGB code. The average is found by summing for all pixels the RGB codes (entrywise) and by dividing the entry by the number of pixels, i.e. the entrywise mean of the RGB code. 

### mosaic_builder.py
We define here the class `Brick` which is going to be our brick.
Each istance stores a length and an optional color. If the length is not provided, it defaults to 1, corresponding to a 1×1 brick.

The module provides a set of functions to generate a brick-based mosaic representation of an image.  
The process starts with `build_plain_mosaic`, which computes the mosaic’s basic grid based on the desired final length of the image. It determines how many bricks are needed horizontally and vertically, and how many pixels each brick should cover to preserve the image proportions.

The `build_mosaic` function divides the image into regions according to this grid and computes the average color of each region. Each region is then assigned the closest color from the chosen palette, producing a two-dimensional list (matrix) of Brick objects (each of length 1) that represents the final mosaic layout.  

Finally, `draw_mosaic` builds this mosaic based on this matrix of bricks. In particular, it draws each brick as a coloured rectangle with the corresponding RGB value and saves the resulting mosaic to the specified output path.

### outputs.py

This module manages the two text outputs. The function `mosaic_instruction` takes as an imput the mosaic matrix and a name (point 2 of *the input* section) and it saves in the folder *output* the file *instructions_name.txt* that contains the "written" mosaic matrix: for every brick (i.e. every entry) in mosaic matrix the file contains in the corresponding entry the label of its color. This file provides a guide for building the actual mosaic.
The function `mosaic_components` has the same input of the previous function and it counts the different bricks of the different colors with this rule: if two consequitive (left to right) bricks have the same color, then they are merged with a max length of 4. This means that this function cuonts how many 1x1, 1x2, 1x3, and 1x4 bricks per color you need to build the mosaic. I made this choice because two 1x1 bricks cost around 16 cents and a single 1x2 costs around 10 cents. Therefore, this is a way to save some money in this process.

## main (project.py)

This file is the main branch of the project and it makes in 8 steps:

1) It reads the .json file containing the palette (a dict of colors) with the function `get_colors`

2) It asks the name of the image you want to build the mosaic and it opens the file.

3) It asks the name under which you want to save the mosaic (it must end with one of the following ('.png', '.jpg', '.jpeg', '.bmp')).

4) It asks the length of the final mosaic in cm (written with or without "cm").

These last 3 steps are in a *while True* loops: the program keeps asking you the input untill you provide a suitable one

5) It builds the mosaic with the functions `build_plain_mosaic` and `build_mosaic`

6) It draws and save the mosaic with `draw_mosaic`

7) It removes the end of the saving name (i.e. the ".png" or similar extension) and it adds to it the ".txt" extension

8) It builds and saves the two text files

I run this project with the portraid "Icarus" by Matisse and I asked for a 25cm mosaic. I used a palette with only yellow, red, blue, and black. I actually built the mosaic, and I'm quite satisfied with the result. 
