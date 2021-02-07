import os
from PIL import Image
import glob

train_path="E:/memelon/doge-training/doge-classification/train/doge"
uniform_size = (600, 600)
i = 0


def checkFileExists(head, filetype):
    global i
    if os.path.isfile(head + "/" + "resized_" + str(i) + filetype):
        i = i + 20
        checkFileExists(head, filetype)


for x in glob.glob(train_path + '/**/*.jpg', recursive=True):
    img = Image.open(x)
    img.thumbnail(uniform_size)
    img = img.resize(uniform_size)
    head, tail = os.path.split(x)
    checkFileExists(head, ".jpg")
    img.save(head + "/" + "resized_" + str(i) + ".jpg", optimize=True, quality=40)
    os.remove(x)
    i = i + 1

for x in glob.glob(train_path + '/**/*.com**', recursive=True):
    img = Image.open(x)
    img.thumbnail(uniform_size)
    img = img.resize(uniform_size)
    head, tail = os.path.split(x)
    checkFileExists(head, ".png")
    img.save(head + "/" + "resized_" + str(i) + ".png", optimize=True, quality=40)
    os.remove(x)
    i = i + 1

for x in glob.glob(train_path + '/**/*.png', recursive=True):
    img = Image.open(x)
    img.thumbnail(uniform_size)
    img = img.resize(uniform_size)
    head, tail = os.path.split(x)
    checkFileExists(head, ".png")
    img.save(head + "/" + "resized_" + str(i) + ".png", optimize=True, quality=40)
    os.remove(x)
    i = i + 1