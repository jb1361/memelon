import glob
import os
from PIL import Image
i = 0

execution_path = os.getcwd()


def checkFileExists(head, filetype):
    global i
    if os.path.isfile(head + "/" + "resized_" + str(i) + filetype):
        i = i + 20
        checkFileExists(head, filetype)


for x in glob.glob(execution_path + 'doge-identification/images/*.jpg', recursive=True):
    img = Image.open(x)
    head, tail = os.path.split(x)
    checkFileExists(head, ".jpg")
    img.save(head + "/" + "renames_" + str(i) + ".jpg", optimize=True, quality=40)
    os.remove(x)
    i = i + 1