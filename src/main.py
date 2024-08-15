import sys
from os import listdir, getcwd
import numpy as np
from PIL import Image
from os.path import isfile, join

print("Importing brisque... this may take a while")
from brisque import BRISQUE

brisque = BRISQUE(url = False)
csv_content = ""


def get_images_path(dir):
    return [join(dir, f) for f in listdir(dir) if isfile(join(dir, f))]


def score_images(image_paths, n: float = None):
    for img_path in image_paths:
        img = Image.open(img_path)
        arr = np.asarray(img)
        scr = brisque.score(img = arr)
        if n == None:
            add_score_to_csv(f"{img_path}:{scr}")
        elif scr <= n:
            add_score_to_csv(f"{img_path}:{scr}")


def add_score_to_csv(content: str):
    global csv_content
    csv_content += f"{content};"


def write_csv(content: str):
    csv_file = open("stats.csv", 'w')
    
    print("Saving stats...")
    csv_file.write(content)
    csv_file.close()
    print("Stats saved!")


args = sys.argv
n = 100

if len(args) == 1:
    print(
            "Incorrect usage! Missing required argument <absolute_directory>\n"
            "Syntax:\n--------\npython main.py <absolute_directory> [n]\n"
            "Parameters:\n-----------\nabsolute_directory: This directory \n"
            "is where the photos are stored\nn: The maximum score allowed score")
    sys.exit(1)
elif len(args) == 3:
    n = args[2]

img_paths = get_images_path(args[1])
score_images(img_paths, n)
write_csv(csv_content)
