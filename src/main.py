import sys
from os import listdir, getcwd
import numpy as np
from PIL import Image
from os.path import isfile, join
import argparse
from brisque import BRISQUE
from rich.progress import Progress

brisque = BRISQUE(url=False)
csv_content = ""


def get_images_path(dir):
    return [join(dir, f) for f in listdir(dir) if isfile(join(dir, f))]


def score_images(image_paths, n: float = None):

    with Progress() as progress:
        task = progress.add_task('[green]Ranking...', total=len(image_paths))

        for img_path in image_paths:
            try:
                img = Image.open(img_path)
                arr = np.asarray(img)
                scr = brisque.score(img=arr)
                if n == None:
                    add_score_to_csv(f"{img_path}:{scr}")
                elif scr <= n:
                    add_score_to_csv(f"{img_path}:{scr}")

                progress.update(task, advance=1)
            except:
                progress.update(task, advance=1)


def add_score_to_csv(content: str):
    global csv_content
    csv_content += f"{content};"


def write_csv(content: str, filepath: str):
    csv_file = open(filepath, "w")

    print("Saving stats...")
    csv_file.write(content)
    csv_file.close()
    print("Stats saved!")


parser = argparse.ArgumentParser(description="Score photos")
parser.add_argument(
    "dir",
)
parser.add_argument(
    "--score",
    metavar="N",
    dest="n",
    action="store_const",
    help="the maximum score allowed",
    default=60,
)
parser.add_argument(
    "-o",
    "--output",
    default="stats.csv",
    help="the output to stats",
)

namespace = parser.parse_args(sys.argv[1:])

img_paths = get_images_path(namespace.dir)
score_images(img_paths, int(namespace.n))
write_csv(csv_content, namespace.output)
