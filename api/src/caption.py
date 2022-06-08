from fileinput import filename
from PIL import Image, ImageDraw, ImageSequence, ImageFont
import io
import os
import textwrap

PROJECT_DIR = os.path.dirname(os.path.abspath(__file__))


def get_background_height(text, width, height, padding, font):
    d = ImageDraw.Draw(Image.new('RGB', (width, height)))
    current_h = padding
    for line in text:
        w, h = d.textsize(line, font=font)
        d.text(((width - w) / 2, current_h), line, font=font, fill='black')
        current_h += h + padding
    return current_h


# TODO: transparent weird?
def caption_gif(text, file_in, file_out, padding=15):

    im = Image.open(file_in)
    width, height = im.size
    fontsize = int(height / 10)
    font = ImageFont.truetype(
        f'{PROJECT_DIR}/fonts/LimerickSerial Xbold.ttf', size=fontsize)
    text = textwrap.wrap(text, width=15)
    background_height = get_background_height(
        text, width, height, padding, font)

    frames = []
    for frame in ImageSequence.Iterator(im):
        b = io.BytesIO()
        frame.save(b, format="GIF")
        frame = Image.open(b)

        base_width, base_height = frame.size

        background = Image.new(
            'RGBA', (base_width, base_height + background_height), (255, 255, 255, 146))

        d = ImageDraw.Draw(background)

        # draw text (centered)
        current_h = padding
        for line in text:
            w, h = d.textsize(line, font=font)
            d.text(((width - w) / 2, current_h), line, font=font, fill='black')
            current_h += h + padding
        del d

        offset = (0, background_height)
        background.paste(frame, offset)

        frames.append(background)

    frames[0].save(file_out, save_all=True, append_images=frames[1:])


# caption_gif('sus', 'gifs/Rotating_earth_(large).gif')
