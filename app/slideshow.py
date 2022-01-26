import time
import numpy as np

from PIL import Image, ImageDraw, ImageFont
from pathlib import Path

class Slideshow:

    def __init__(self, output_device):
        self.output_device=output_device
        self.height=576
        self.width=1024
        self.images=[]
        self.current_counter = 0

    def show(self, img:Image.Image):
        # reset the image
        # self.img = Image.new('RGBA', (self.height, self.width), color = (66,66,66))
        with open(self.output_device, 'rb+') as buf:
            buf.write(np.asarray(self.img.getdata(),dtype=np.uint8))
    
    def add_image(self, path:str):
        self.images.insert(self.current_counter, path)

    def start_slideshow(self):
        while True:
            if len(self.images)>0:
                img = Image.open(self.images[self.current_counter])
                self.show(img)
                self.current_counter +=1
                if self.current_counter > len(self.images):
                    self.current_counter = 0
            time.sleep(10)
        
if __name__ == "__main__":
    fb = Slideshow('/dev/fb0')
    fb.start_slideshow()
