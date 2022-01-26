import time
import logging
import glob
import numpy as np

from PIL import Image

class Slideshow:

    def __init__(self, output_device):
        logging.basicConfig()
        self._logger = logging.getLogger(__name__)
        self._logger.setLevel(logging.DEBUG)
        self._logger.info('Instantiated Slideshow')

        self.output_device=output_device
        self.width=1824        
        self.height=984
        self.images=glob.glob('./photos/*.png')
        self.current_counter = 0
        self._logger.info('image list: %s', self.images)

    def show(self, img:Image.Image):
        self._logger.info('showing an image')
        with open(self.output_device, 'rb+') as buf:
            buf.write(np.swapaxes(np.asarray(img.getdata(),dtype=np.uint8),0,2))
    
    def add_image(self, path:str):
        self.images.insert(self.current_counter, path)

    def start_slideshow(self):
        self._logger.info('Started slideshow')

        while True:
            if len(self.images)>0:
                print(f'opening image: {self.images[self.current_counter]}')
                img = Image.open(self.images[self.current_counter]).resize(size=(self.width,self.height))

                self.show(img)
                self.current_counter +=1
                if self.current_counter >= len(self.images):
                    self.current_counter = 0
            time.sleep(10)
