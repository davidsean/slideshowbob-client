
import os
import requests
import logging

from io import BytesIO
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont


class MessageProcessor:

    def __init__(self, image_url:str, sender_id:str, thumnail_size=200):
        logging.basicConfig()
        self._logger = logging.getLogger(__name__)
        self._logger.setLevel(logging.DEBUG)
        self._logger.info("Instantiated MessageProcessor")

        self.thumbnail_size=thumnail_size
        self.font_path = Path(__file__).parent.joinpath('static/Roboto-Regular.ttf').absolute()
        self.image_url = image_url
        self.sender_id = sender_id
        self.name = None
        self.profile_pic = None
        # set name and profile pic
        self.get_user_data()
        if self.name is None or self.profile_pic is None:
            self._logger.warning('unable to fetch user data, aborting')
            return

    def process_post(self):
        """ Process the post
        """
        if self.name is not None and self.profile_pic is not None:
            posted_img = self.download_image(self.image_url)
            profile_img = self.download_image(self.profile_pic)
            return self.create_image_montage(posted_img, profile_img)
        else:
            self._logger.info('missing user data')
    
    def create_image_montage(self, posted_image:Image.Image, profile_image:Image.Image) -> Image.Image:
        """Create montage with user profile pic, username and submitted image

        Args:
            posted_image (Image.Image): The image the user posted
            profile_image (Image.Image): The profile pic

        Returns:
            Image.Image: A resulting combined (profile pic, name and posted) image.
        """
        if self.name is not None and self.profile_pic is not None:
            profile_image.thumbnail((self.thumbnail_size, self.thumbnail_size))
            # start with black image 
            montage = Image.new("RGB", (posted_image.size[0]+self.thumbnail_size,posted_image.size[1]+self.thumbnail_size), (0,0,0))
            montage.paste(profile_image, (0,0))
            montage.paste(posted_image, (self.thumbnail_size, self.thumbnail_size))
            title = ImageDraw.Draw(montage)
            font = ImageFont.truetype(str(self.font_path), 90)
            title.text((self.thumbnail_size, 10), self.name, font=font, fill =(255, 255, 255))
            return montage
        else:
            self._logger.info('missing user data')

    def download_image(self, image_url:str) -> Image.Image:
        """Downloads the image at the URL

        Args:
            image_url (str): The image URL

        Returns:
            Image.Image: A PIL Image object
        """
        data = requests.get(image_url).content
        img = Image.open(BytesIO(data))
        return img
     
    def get_user_data(self):
        """ get username and profile image URL

        Returns:
            Tuple (name, profile_url): A String tuple with the name and profile URL
        """
        PAGE_ACCESS_TOKEN = os.environ.get('PAGE_ACCESS_TOKEN')
        url = f'https://graph.facebook.com/{self.sender_id}?fields=name,profile_pic&access_token={PAGE_ACCESS_TOKEN}'
        res = requests.get(url)
        if res.status_code == 200 and 'application/json' in res.headers.get('Content-Type',''):
            json_res = res.json()
            self.name = str(json_res['name'])
            self.profile_pic = str(json_res['profile_pic'])
