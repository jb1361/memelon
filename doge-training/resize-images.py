import os
from PIL import Image
import glob

train_path="E:/memelon/doge-training/doges/"
uniform_size = (400, 400)
i = 0
for x in glob.glob(train_path + '/**/*.png', recursive=True):
    img = Image.open(x)
    img.thumbnail(uniform_size)
    img = img.resize(uniform_size)
    head, tail = os.path.split(x)
    img.save(head + "/" + "resized_" + str(i) + ".png", optimize=True, quality=40)
    os.remove(x)
    i = i + 1

for x in glob.glob(train_path + '/**/*.jpg', recursive=True):
    img = Image.open(x)
    img.thumbnail(uniform_size)
    img = img.resize(uniform_size)
    head, tail = os.path.split(x)
    img.save(head + "/" + "resized_" + str(i) + ".jpg", optimize=True, quality=40)
    os.remove(x)
    i = i + 1

