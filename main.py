#!/usr/bin/python
# -*- coding:utf-8 -*-
import sys
import os
import requests


picdir = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'pic')
libdir = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'lib')
if os.path.exists(libdir):
    sys.path.append(libdir)

import logging
from waveshare_epd import epd7in5_V2
import time
from PIL import Image,ImageDraw,ImageFont
import traceback


TICKER_API_URL = 'https://api.coinmarketcap.com/v1/ticker/'

def get_latest_crypto_info(crypto):
  response = requests.get("https://api.coingecko.com/api/v3/coins/markets?vs_currency=eur&ids="+crypto+"")
  response_json = response.json()
  return response_json




logging.basicConfig(level=logging.DEBUG)

try:
    logging.info("epd7in5_V2 Demo")
    epd = epd7in5_V2.EPD()

    logging.info("init and Clear")
    epd.init()
    epd.Clear()

    def draw():
        font_large = ImageFont.truetype(os.path.join(picdir, 'Font.ttc'), 35)
        font18 = ImageFont.truetype(os.path.join(picdir, 'Font.ttc'), 18)

        # Drawing on the Horizontal image
        logging.info("1.Drawing on the Horizontal image...")
        Himage = Image.new('1', (epd.width, epd.height), 255)  # 255: clear the frame
        draw = ImageDraw.Draw(Himage)

        from datetime import datetime

        now = datetime.now()

        current_time = now.strftime("%H:%M")

        draw.text((350, 10), current_time, font = font_large, fill = 0)

        margin = 20
        i=1
        while i<2:
            draw.text((10, i*45+margin), 'Crypto', font = font_large, fill = 0)
            i=i+1
        crypto_currencies = ['bitcoin', 'ethereum', 'zcash', 'eos']
        for c in crypto_currencies:
            draw.text((10, i*45+margin), c+": ", font = font_large, fill = 0)
            draw.text((210, i*45+margin), str(get_latest_crypto_info(c)[0]['current_price'])+" EUR", font = font_large, fill = 0)
            i=i+1

        epd.display(epd.getbuffer(Himage))
        time.sleep(20)

        logging.info("Clear...")
        epd.init()
        epd.Clear()

    while 1 == 1:
        draw()

    logging.info("Goto Sleep...")
    epd.sleep()
    time.sleep(3)

    epd.Dev_exit()

except IOError as e:
    logging.info(e)

except KeyboardInterrupt:
    logging.info("ctrl + c:")
    epd7in5_V2.epdconfig.module_exit()
    exit()