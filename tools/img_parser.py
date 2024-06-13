path = "files"
size = 640

import os, sys
from PIL import Image
import numpy as np


files = os.listdir(path)
for file in files:
    sub = Image.open(path + "/" + file)
    sub = sub.convert("RGB")
    data = np.array(sub)
    red, green, blue = data.T
    data = np.array([blue, green, red])
    data = data.transpose()
    sub = Image.fromarray(data)

    sub.save(path + "/" + file)
