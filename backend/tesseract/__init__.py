#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function

from .tesseract  import image_to_string
from .builders import WordBoxBuilder

from PIL import Image, ImageEnhance
import io
from PyQt5 import QtWidgets, QtCore
import re

screenshot_width = 600
screenshot_height = 100

LANGUAGE_OCR_DICT = {
    "af" : "tesseract-ocr-afr",
    "ar" : "tesseract-ocr-ara",
    "az" : "tesseract-ocr-aze",
    "be" : "tesseract-ocr-bel",
    "bn" : "tesseract-ocr-ben",
    "bg" : "tesseract-ocr-bul",
    "ca" : "tesseract-ocr-cat",
    "cs" : "tesseract-ocr-ces",
    "zh-CN" : "tesseract-ocr-chi-sim",
    "zh-TW" : "tesseract-ocr-chi-tra",
    "da" : "tesseract-ocr-dan",
    "de" : "tesseract-ocr-deu",
    "gr" : "tesseract-ocr-ell",
    "en" : "tesseract-ocr-eng",
    "eo" : "tesseract-ocr-epo",
    "et" : "tesseract-ocr-est",
    "eu" : "tesseract-ocr-eus",
    "fi" : "tesseract-ocr-fin",
    "fr" : "tesseract-ocr-fra",
    "gl" : "tesseract-ocr-glg",
    "iw" : "tesseract-ocr-heb",
    "hi" : "tesseract-ocr-hin",
    "hr" : "tesseract-ocr-hrv",
    "id" : "tesseract-ocr-ind",
    "is" : "tesseract-ocr-isl",
    "it" : "tesseract-ocr-ita",
    "ja" : "tesseract-ocr-jpn",
    "kn" : "tesseract-ocr-kan",
    "ko" : "tesseract-ocr-kor",
    "lv" : "tesseract-ocr-lav",
    "lt" : "tesseract-ocr-lit",
    "mk" : "tesseract-ocr-mkd",
    "mt" : "tesseract-ocr-mlt",
    "ms" : "tesseract-ocr-msa",
    "nl" : "tesseract-ocr-nld",
    "no" : "tesseract-ocr-nor",
    "pl" : "tesseract-ocr-pol",
    "pt" : "tesseract-ocr-por",
    "ro" : "tesseract-ocr-ron",
    "ru" : "tesseract-ocr-rus",
    "sk" : "tesseract-ocr-slk",
    "sl" : "tesseract-ocr-slv",
    "es" : "tesseract-ocr-spa",
    "sq" : "tesseract-ocr-sqi",
    "sr" : "tesseract-ocr-srp",
    "sw" : "tesseract-ocr-swa",
    "sv" : "tesseract-ocr-swe",
    "ta" : "tesseract-ocr-tam",
    "te" : "tesseract-ocr-tel",
    "th" : "tesseract-ocr-tha",
    "tr" : "tesseract-ocr-tur",
    "vi" : "tesseract-ocr-vie",
    }

class OcrWord(QtCore.QObject):
    def __init__(self, app):
        QtCore.QObject.__init__(self)
        self.screen = app.primaryScreen()
        self.screen_width = self.screen.size().width()
        self.screen_height = self.screen.size().height()

    def capture_screen(self, x=0, y=0, width=None, height=None):
        if width == None: width = self.screen_width
        if height == None: height = self.screen_height

        qpixmap = self.screen.grabWindow(0, x, y, width, height)
        return qpixmap.toImage()

    def qimage_to_pil_image(self, image):
        buffer = QtCore.QBuffer()
        buffer.open(QtCore.QIODevice.ReadWrite)
        image.save(buffer, "PNG")

        strio = io.BytesIO()
        strio.write(buffer.data())
        buffer.close()
        strio.seek(0)
        return Image.open(strio)

    def filter_punctuation(self, text, src_lang):
        if src_lang in ["en"]:
            return re.sub("[^A-Za-z_-]", " ", text).strip().split(" ")[0]
        else:
            return text

    def recognize(self, mouse_x, mouse_y, src_lang):
        x = max(mouse_x - screenshot_width / 2, 0)
        y = max(mouse_y - screenshot_height / 2, 0)
        width = min(mouse_x + screenshot_width / 2, self.screen_width) - x
        height = min(mouse_y + screenshot_height / 2, self.screen_height) - y

        scale = 2

        ocr_pkg_name = LANGUAGE_OCR_DICT[src_lang]
        lang = ocr_pkg_name.split("tesseract-ocr-")[1].replace("-", "_")

        qimage = self.capture_screen(x, y, width, height)

        image = self.qimage_to_pil_image(qimage)
        image = image.convert("L").resize((int(width * scale), int(height * scale)))
        image = ImageEnhance.Contrast(image).enhance(1.5)

        word_boxes = image_to_string(
            image,
            lang=lang,
            builder=WordBoxBuilder())

        cursor_x = (mouse_x - x) * scale
        cursor_y = (mouse_y - y) * scale

        for word_box in word_boxes[::-1]:
            ((left_x, left_y), (right_x, right_y)) = word_box.position
            if (left_x <= cursor_x <= right_x and left_y <= cursor_y <= right_y):
                word = self.filter_punctuation(word_box.content, src_lang)
                # Return None if ocr word is space string.
                if word.isspace():
                    return None
                else:
                    return word

        return None
