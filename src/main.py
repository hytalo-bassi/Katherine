import sys
from os import listdir, getcwd
import numpy as np
from PIL import Image
from os.path import isfile, join

print("Importing brisque... this may take a while")
from brisque import BRISQUE

brisque = BRISQUE(url = False) 


def get_images_path(dir):
    return [join(dir, f) for f in listdir(dir) if isfile(join(dir, f))]


def score_images(image_paths, n: float = None):
    for img_path in image_paths:
        img = Image.open(img_path)
        arr = np.asarray(img)
        scr = brisque.score(img = arr)
        if n == None:
            print(img_path, scr)
        elif scr <= n:
            print(img_path, scr)


args = sys.argv
n = 100

if len(args) == 1:
    print()
    print("Incorrect usage! Missing required argument <absolute_directory>")
    print("python main.py <absolute_directory> [n]")
    print("Parameters\nabsolute_directory: The directory where Katherine will look"
          "(must be in the same working directory)\n"
          "n: the maximum score to be printed")
    sys.exit(1)
elif len(args) == 3:
    n = args[2]

img_paths = get_images_path(args[1])
score_images(img_paths, n)
