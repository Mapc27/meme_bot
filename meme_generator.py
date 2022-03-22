import os
from typing import List

from PIL import Image, ImageFont, ImageDraw

from config import IMAGES_FOLDER_NAME


class MemeGenerator:
    instances: List = []

    def __init__(self):
        self.instances.append(self)

        self.image: Image = None
        self.file_name: str = ''
        self.draw: ImageDraw.Draw = None
        self.font: ImageFont = None

        self.top_caption: str = ''
        self.bottom_caption: str = ''

        self.authors: List[int] = []

    @classmethod
    def add_something(cls, chat_id: int, image: str = '', caption: str = ''):
        if image and caption or not image and not caption:
            raise AttributeError("choose only one of fields image and text")

        instance: MemeGenerator

        if image:
            for instance in cls.instances:
                if instance.need_image() and not instance.have_author(chat_id):
                    instance.add_image(image)
                    instance.add_author(chat_id)
                    return instance

            instance = MemeGenerator()
            instance.add_image(image)
            instance.add_author(chat_id)

            return instance

        if caption:
            for instance in cls.instances:
                if instance.need_caption() and not instance.have_author(chat_id):
                    instance.add_caption(caption)
                    instance.add_author(chat_id)
                    return instance

            instance = MemeGenerator()
            instance.add_caption(caption)
            instance.add_author(chat_id)

            return instance

    def remove_instance(self):
        try:
            self.instances.remove(self)
            del self
        except ValueError:
            raise ValueError("instance doesn't exists in cls.instances list")

    def add_image(self, file_name: str):
        if self.image:
            raise AttributeError('image already exists')

        if not os.path.exists(f"{IMAGES_FOLDER_NAME}/{file_name}"):
            raise FileExistsError(f"'{file_name}' doesn't exists in /images folder")

        self.image = Image.open(f"{IMAGES_FOLDER_NAME}/{file_name}")
        self.file_name = file_name
        self.draw = ImageDraw.Draw(self.image)
        self.font = ImageFont.truetype("impact.ttf", 42)

    def add_caption(self, caption: str):
        if not self.need_caption():
            raise AttributeError('All captions already exists')

        if not self.top_caption:
            self.top_caption = caption

        elif not self.bottom_caption:
            self.bottom_caption = caption

    def add_author(self, chat_id: int):
        if len(self.authors) > 2:
            raise AttributeError("Max authors number is 3")

        if len(self.authors) < 0:
            raise AttributeError("Authors number can't be less than 0")

        if self.have_author(chat_id):
            raise AttributeError("This author already exists")

        self.authors.append(chat_id)

    def need_image(self):
        return False if self.image else True

    def need_caption(self):
        return False if self.top_caption and self.bottom_caption else True

    def ready(self):
        return True if self.image and self.top_caption and self.bottom_caption else False

    def have_author(self, chat_id: int):
        return chat_id in self.authors

    def generate(self):
        if self.need_image():
            raise AttributeError("image doesn't exists")

        if self.need_caption():
            raise AttributeError("Need more captions")

        if len(self.authors) != 3:
            raise AttributeError("Authors number less or more than 3")

        self.write_top_caption()
        self.write_bottom_caption()
        self.image.save(f"{IMAGES_FOLDER_NAME}/{self.file_name}")

        return self.file_name

    def write_top_caption(self):
        text = self.top_caption
        text = text.upper()
        text_width, text_height = self.draw.textsize(text, self.font)

        print(self.image.width, self.image.height)
        print(text_width, text_height)

        coord_x = (self.image.width - text_width) // 2
        coord_y = 7

        self.draw.text((coord_x, coord_y), text, (255, 255, 255), font=self.font)

    def write_bottom_caption(self):
        text = self.bottom_caption
        text = text.upper()
        text_width, text_height = self.draw.textsize(text, self.font)

        print(self.image.width, self.image.height)
        print(text_width, text_height)

        coord_x = (self.image.width - text_width) // 2
        coord_y = self.image.height - 7 - text_height

        self.draw.text((coord_x, coord_y), text, (255, 255, 255), font=self.font)


if __name__ == '__main__':
    meme_generator = MemeGenerator()
    meme_generator.add_something(1, image='image.jpeg')
    meme_generator.add_something(2, caption="One does not simplyfd")
    generator = meme_generator.add_something(3, caption="One does not")
    if generator.ready():
        print(meme_generator.generate())
