#! /usr/bin/python3
# behrouz_ashraf
# garpozir@gmail.com

import os
from PIL import Image, ImageChops

def crp(sv):
    im = Image.open(f'{sv}.png')
    width, height = im.size
    left = 5
    top = height / 2 + 30
    right = width / 4
    bottom = 3 * height / 3
    im1 = im.crop((left, top, right, bottom))
    im1.save(f'{sv}.png')

class W_r:
    def __init__(self, address):
        self.address = address

    def dell(self):
        if os.path.exists(self.address):
            os.remove(self.address)
