import os
from PIL import Image

directory = "C:\\Users\\harno\\Desktop\\DDM-data\\seq2\\frames"
"""
Enter full path of directory
"""
no_of_divisions = 2
"""
This must be a integer, not a string
"""


def crop(directory, filename, number):
    path = os.path.join(directory, filename)
    im = Image.open(path)
    w, h = im.size
    unit = w // number
    # if unit - round(unit) != 0:
    #     print("There will be some pixels lost, since \
    #         the number of divisions you chose is not \
    #         dividing the original image in whole numbers.")
    for i in range(number):
        im1 = im.crop((unit * i, 0, unit * (i+1), h))
        name = filename.name[:-4] + ".tif"
        child_dir = str(directory) + "-" + str(i+1)
        path = os.path.join(directory, child_dir, name)
        im1.save(path)

for i in range(no_of_divisions):
    child_dir = str(directory) + "-" + str(i+1)
    path = os.path.abspath(child_dir)
    if not os.path.exists(path):
        os.mkdir(path)

for filename in os.scandir(directory):
    if filename.is_file():
        crop(directory, filename, no_of_divisions)
