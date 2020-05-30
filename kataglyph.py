# Created by Mario Schädel
# mario.schaedel@gmail.com
# mcranium.github.io

# The progamm is free and open software (GNU GPL license Version 3).

# Command line functionality adopted from:
# https://towardsdatascience.com/how-to-write-python-command-line-interfaces-like-a-pro-f782450caf0d

import skimage
from skimage import io
import numpy as np
import os


import click
from funcy import identity

@click.command()
@click.option("--in", "-i", "in_file", required=True,
    help="Path to the input image (red-cyan stereo anaglyph).",
    type=click.Path(exists=True, dir_okay=False, readable=True),
)
@click.option("--out-file", "-o", default="./output.gif",
    help="Path to animated gif file to store the result.",
    type=click.Path(dir_okay=False),
)
@click.option("-v", "--verbose", is_flag=True, help="Verbose output")

@click.option("-f", "--frames_per_second", default=4,
    help="Adjust the speed of the GIF animation in frames per second. The default value is 4 fps")


def process(in_file, out_file, frames_per_second, verbose):
    """ Processes the input file IN and stores the result to
    output file OUT.
    """

    print_func = print if verbose else identity

    print_func("Reading input file")
    filename = os.path.join(skimage.data_dir, in_file)
    danica = io.imread(filename)

    print_func("Making copies and deleting color channels")
    danica_right = danica.copy()
    danica_right[:,:,0] = np.zeros([danica.shape[0],danica.shape[1]])

    danica_left = danica.copy()
    danica_left[:,:,1] = np.zeros([danica.shape[0],danica.shape[1]])
    danica_left[:,:,2] = np.zeros([danica.shape[0],danica.shape[1]])

    print_func("Desaturating left and right images")
    from skimage.color import rgb2gray
    danica_left = rgb2gray(danica_left)
    danica_right = rgb2gray(danica_right)

    print_func("Matching the histograms of the left and right images")
    from skimage.exposure import match_histograms
    danica_left_m = match_histograms(danica_left, danica_right, multichannel=True)

    print_func("Combining the left and right images to a sequence")
    import imageio
    frames = []
    frames.append(danica_left_m)
    frames.append(danica_right)

    print_func("Saving the sequence as a .gif file")
    imageio.mimsave(out_file, frames, fps=frames_per_second)

if __name__ =="__main__":
    process()
