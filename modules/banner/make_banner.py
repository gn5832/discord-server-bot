import os
import io
from PIL import Image, ImageDraw, ImageFont
from modules.configs.banner_config import *




class BaseBanner:
    BASE_DIR = os.getcwd()
    BANNER_PATH = os.path.join(BASE_DIR, 'modules', 'banner', 'data', 'images', BANNER_FILENAME)
    FONT_PATH = os.path.join(BASE_DIR, 'modules', 'banner', 'data', 'fonts', FONT_FILENAME)
    FONT = ImageFont.truetype(FONT_PATH, size=FONT_SIZE)

    def get_text_offset(self, text: str|int):
        '''В зависимости от размера шрифта и длинны текста, вычисляет кол-во пикселей,
        на которое нужно сдвинуть текст в левую сторону, что бы он был по центру.
        '''
        return round((FONT_SIZE / 4) * (len(str(text)) - 1))


    def banner_make(self, in_voice_members_len: int):
        banner = Image.open(self.BANNER_PATH)
        banner.load()
        draw_text = ImageDraw.Draw(banner)

        
        coords = (IN_VOICE_COORDS[0] - self.get_text_offset(in_voice_members_len), IN_VOICE_COORDS[1])


        draw_text.text(
            coords,
            str(in_voice_members_len),
            font=self.FONT,
            fill=(IN_VOICE_TEXT_COLOR),
            align=IN_VOICE_TEXT_ALIGN
            )
        return banner



class GifBanner(BaseBanner):



    def to_bytes(cls, images: list):
        result = io.BytesIO()
        img = images[0]
        img.save(result, save_all=True, format='GIF', append_images=images, duration=100, loop=0)
        return result.getvalue()


    def get_count_step(self, in_voice_members_len: str):
        frames = GIF_COUNT_SECONDS * 10
        count_step = in_voice_members_len // frames
        return count_step if count_step else 1




    
    def make(self, in_voice_members_len: int):
        images = []

        image = self.banner_make(in_voice_members_len)
        images.append(image)
        
        for _in_voice_members_len in range(0, in_voice_members_len, self.get_count_step(in_voice_members_len)):
            image = self.banner_make(_in_voice_members_len)
            images.append(image)


        for _ in range(STATIC_END_FRAMES):
            image = self.banner_make(in_voice_members_len)
            images.append(image)

        return self.to_bytes(images)


class PngBanner(BaseBanner):

    def to_bytes(cls, image: Image):
        result = io.BytesIO()
        image.save(result, format='PNG')
        return result.getvalue()


    def make(self, in_voice_members_len: int):
        banner_image = self.banner_make(in_voice_members_len)
        return self.to_bytes(banner_image)
