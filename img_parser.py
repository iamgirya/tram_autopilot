path = "datasets/tram_sim/images"
size = 640

import os, sys
from PIL import Image


files = os.listdir(path)
for file in files:
    base_h = 640
    img = Image.open(path + "/" + file)
    wpercent = base_h / float(img.size[1])
    wsize = int((float(img.size[0]) * float(wpercent)))
    img = img.resize((wsize, base_h), Image.Resampling.LANCZOS)
    img.save(path + "/" + file)
