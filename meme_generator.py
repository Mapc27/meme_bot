from typing import List

from PIL import Image, ImageFont, ImageDraw


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

    def add_image(self, file_name: str):
        if self.image:
            raise AttributeError('image already exists')

        self.image = Image.open(f"images/{file_name}")
        self.file_name = file_name
        self.draw = ImageDraw.Draw(self.image)
        self.font = ImageFont.truetype("impact.ttf", 42)

    def add_caption(self, caption: str):
        if not self.top_caption:
            self.top_caption = caption

        elif not self.bottom_caption:
            self.bottom_caption = caption

        else:
            raise AttributeError('All captions already exists')

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
            raise AttributeError("'image' doesn't exists")

        if self.need_caption():
            raise AttributeError("Need more captions")

        if len(self.authors) != 3:
            raise AttributeError("Authors number less or more than 3")

        self.draw_text(self.top_caption, 'top')
        self.draw_text(self.bottom_caption, 'bottom')
        self.image.save(f"images/{self.file_name}")

        return self.file_name

    def draw_text_with_outline(self, text, x, y):
        self.draw.text((x - 2, y - 2), text, (0, 0, 0), font=self.font)
        self.draw.text((x + 2, y - 2), text, (0, 0, 0), font=self.font)
        self.draw.text((x + 2, y + 2), text, (0, 0, 0), font=self.font)
        self.draw.text((x - 2, y + 2), text, (0, 0, 0), font=self.font)
        self.draw.text((x, y), text, (255, 255, 255), font=self.font)

    def draw_text(self, text, pos):
        text = text.upper()
        width, height = self.draw.textsize(text, self.font)

        line_count = 1
        if width > self.image.width:
            line_count = int(round((width / self.image.width) + 1))

        print("line_count: {}".format(line_count))

        lines = []
        if line_count > 1:

            last_cut = 0
            is_last = False
            for i in range(0, line_count):
                if last_cut == 0:
                    cut = (len(text) / line_count) * i
                else:
                    cut = last_cut

                if i < line_count - 1:
                    next_cut = (len(text) / line_count) * (i + 1)
                else:
                    next_cut = len(text)
                    is_last = True

                print("cut: {} -> {}".format(cut, next_cut))

                # make sure we don't cut words in half
                if next_cut == len(text) or text[next_cut] == " ":
                    print("may cut")
                else:
                    print("may not cut")
                    while text[next_cut] != " ":
                        next_cut += 1
                    print("new cut: {}".format(next_cut))

                line = text[cut:next_cut].strip()

                # is line still fitting ?
                width, height = self.draw.textsize(line, self.font)
                if not is_last and width > self.image.width:
                    print("overshot")
                    next_cut -= 1
                    while text[next_cut] != " ":
                        next_cut -= 1
                    print("new cut: {}".format(next_cut))

                last_cut = next_cut
                lines.append(text[cut:next_cut].strip())

        else:
            lines.append(text)

        print(lines)

        last_y = -height
        if pos == "bottom":
            last_y = self.image.height - height * (line_count + 1) - 10

        for i in range(0, line_count):
            width, height = self.draw.textsize(lines[i], self.font)
            x = self.image.width / 2 - width / 2
            y = last_y + height
            self.draw_text_with_outline(lines[i], x, y)
            last_y = y


if __name__ == '__main__':
    meme_generator = MemeGenerator()
    meme_generator.add_image('image.jpeg')
    meme_generator.add_caption("One does not simplyfd fdf dfgtr rt hrhrh rth rth rt")
    meme_generator.add_caption("One does not simplyfd fdf dfgtr rt hrhrh rth rth rt ")

    meme_generator.generate()
