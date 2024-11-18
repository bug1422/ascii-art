import cv2 as cv
import numpy as np
from typing import Final
from fastapi import UploadFile
from PIL import Image, ImageFont, ImageDraw
from io import BytesIO
import base64
from math import floor


class Converter:
    def __init__(self, image: UploadFile, size) -> None:
        self.density: Final[str] = "Ñ@#W$9876543210?!abc;:+=-,._ "
        self.image = image
        self.file = image.file
        self.font_size = size
        self.margin = len(self.density) - 1

    def convert(self) -> str:
        stream = np.asarray(bytearray(self.file.read()), dtype=np.uint8)
        img = cv.imdecode(stream, cv.IMREAD_COLOR)
        gray_scaled = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
        org_h, org_w = img.shape[:2]
        h = floor(org_h / self.font_size * 2)
        w = floor(org_w / self.font_size * 2)
        resized = cv.resize(
            gray_scaled,
            (h, w),
            interpolation=cv.INTER_LINEAR,
        )
        result = Image.new("RGB", (org_w, org_h))
        draw = ImageDraw.Draw(result)
        font = ImageFont.load_default(self.font_size)
        for y in range(resized.shape[0]):
            for x in range(resized.shape[1]):
                color = img[
                    min(y * self.font_size, org_h - 1),
                    min(x * self.font_size, org_w - 1),
                ]
                text_density = self.density[round(resized[y][x] / 255 * self.margin)]
                draw.text(
                    (x * self.font_size, y * self.font_size),
                    text_density,
                    fill=(color[2], color[1], color[0]),  # BGR to RGB
                    font=font,
                )
        result_stream = BytesIO()
        result.save(result_stream, format="PNG")
        result_stream.seek(0)
        return base64.b64encode(result_stream.read()).decode()
