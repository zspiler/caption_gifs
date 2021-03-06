from fileinput import filename
from PIL import Image, ImageDraw, ImageSequence, ImageFont, ImageChops
import io
import os
import math
import textwrap
from transparent_gif_converter import save_transparent_gif

PROJECT_DIR = os.path.dirname(os.path.abspath(__file__))


def get_background_height(text, width, height, padding, margin, font):
    d = ImageDraw.Draw(Image.new('RGB', (width, height)))
    current_h = margin
    for line in text:
        w, h = d.textsize(line, font=font)
        d.text(((width - w) / 2, current_h), line, font=font, fill='black')
        current_h += h
    return current_h + margin + padding


def get_max_line_width(width, font):
    d = ImageDraw.Draw(Image.new('RGB', (100, 100)))
    max_letter_width, _ = d.textsize('a', font=font)
    return int(math.ceil(width / max_letter_width))


# NOTE: Credit: https://stackoverflow.com/questions/10689512/determining-if-a-gif-is-transparent-in-python
def gif_uses_transparency(filename):
    img = Image.open(filename)
    trans = img.info.get("transparency", None)
    if trans is not None:
        trans *= 3  # convert color number to palette table index
        palette = img.getpalette()
        imgs = []
        for bg in [0, 255]:   # map transparent color first to black, then white
            palette[trans:trans+3] = [bg] * 3
            img.putpalette(palette)
            imgs.append(img.convert("L"))
        return bool(ImageChops.difference(*imgs).getbbox())
    return False


def caption_gif(text, file_in, file_out, speedup=False, dark_background=False):

    gif = Image.open(file_in)

    background_color = (0, 0, 0, 255) if dark_background else (
        255, 255, 255, 255)
    text_color = (255, 255, 255, 255) if dark_background else (0, 0, 0, 255)

    width, height = gif.size
    margin = int(math.ceil(height * 0.05))
    padding = int(math.ceil(height * 0.01))

    fontsize = int(height / 10) if height/10 >= 15 else 15

    font = ImageFont.truetype(
        f'{PROJECT_DIR}/fonts/LimerickSerial Xbold.ttf', size=fontsize)

    text = textwrap.wrap(text, width=get_max_line_width(width, font))  # was 15
    background_height = get_background_height(
        text, width, height, padding, margin, font)

    frames = []
    for frame in ImageSequence.Iterator(gif):
        b = io.BytesIO()
        frame.save(b, format="GIF")
        frame = Image.open(b)

        base_width, base_height = frame.size

        background = Image.new(
            'RGBA', (base_width, base_height + background_height), background_color)

        d = ImageDraw.Draw(background)

        current_h = margin
        for line in text:
            w, h = d.textsize(line, font=font)
            d.text(((width - w) / 2, current_h),
                   line, font=font, fill=text_color)
            current_h += h + padding
        del d

        offset = (0, background_height)
        background.paste(frame, offset)

        frames.append(background)

    duration = gif.info['duration'] / 2 if speedup else gif.info['duration']

    if gif_uses_transparency(file_in):
        durations = [duration for _ in range(len(frames))]
        save_transparent_gif(frames[1:], durations, file_out)
        return

    frames[0].save(file_out, save_all=True,
                   append_images=frames[1:], loop=0, duration=duration)
