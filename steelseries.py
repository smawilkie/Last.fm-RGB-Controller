# https://github.com/slattery-mark/SteelSeries-CKL-App

from json import load
from os import getenv
import threading
from time import sleep
from requests import Session, post
from PIL import Image

class CKL:
    def __init__(self):
        corePropsPath = getenv('PROGRAMDATA') + "\SteelSeries\SteelSeries Engine 3\coreProps.json" 
        self.sseAddress = f'http://{load(open(corePropsPath))["address"]}'
        self.game = 'CUSTOM_KEYBOARD_LIGHTING'
        self.game_display_name = 'Custom Keyboard Lighting'
        self.event = 'BITMAP_EVENT'

        self.outline = [[[0, 0, 0] for i in range(15)] for j in range(6)]

        self.keys = [
        0,   2,   3,   4,   5,   6,   7,   8,   9,   11,  12,  13,  14,  37,
        22,  23,  24,  25,  26,  27,  28,  29,  30,  31,  32,  33,  34,  35,  38,
        44,  45,  46,  47,  48,  49,  50,  51,  52,  53,  54,  55,  56,  57,  39,
        66,  67,  68,  69,  70,  71,  72,  73,  74,  75,  76,  77,  79,  61,
        88,  90,  91,  92,  93,  94,  95,  96,  97,  98,  99,  101, 104, 60,
        110, 111, 112, 116, 121, 120, 122, 124, 125, 126, 127
        ]

        self.registerGame()
        self.bindGameEvent()

    def bindGameEvent(self):
        """Binds a lighting event to Engine."""
        endpoint = f'{self.sseAddress}/bind_game_event'
        payload = {
            "game": self.game,
            "event": self.event,
            "value_optional": r'"true"',
            "handlers": [
                {
                    "device-type": "rgb-per-key-zones",
                    "zone": "all",
                    "mode": "bitmap"
                }
            ]
        }
        post(endpoint, json=payload)        

    def registerGame(self):
        """Registers this application to Engine."""
        endpoint = f'{self.sseAddress}/game_metadata'
        payload = {
            "game" : self.game,
            "game_display_name" : self.game_display_name,
            "developer" : "yrfriendmark"
        }
        post(endpoint, json=payload)

    def setLightingArray(self):
        endpoint = f'{self.sseAddress}/game_event'
        frame = [[0, 0, 0] for i in range(132)]
               
        usedColours = [self.outline[0][i] for i in range(14)] + \
                      [self.outline[1][i] for i in range(15)] + \
                      [self.outline[2][i] for i in range(15)] + \
                      [self.outline[3][i] for i in range(12)] + [self.outline[3][i] for i in range(13, 15)] + \
                      [self.outline[4][i] for i in range(12)] + [self.outline[4][i] for i in range(13, 15)] + \
                      [self.outline[5][i] for i in range(0, 3)] + [self.outline[5][i] for i in range(5, 10)] + [self.outline[5][i] for i in range(12, 15)]

        for index, key in enumerate(self.keys):
            frame[key] = [*usedColours[index]]

        payload = {
            "game": self.game,
            "event": self.event,
            "data" : {
                "value" : 255,
                "frame" : {
                    "bitmap" : frame
                }
            }
        }

        with Session() as s:
            s.post(endpoint, json=payload)


ckl = CKL()

def set(filename: str):
    pixels = Image.open(f"{filename}/15x6.png").load()
    colours = []
    for y in range(6):
        currentRow = []
        for x in range(15):
            currentRow.append(pixels[x, y])
        colours.append(currentRow)
    ckl.outline = colours
    ckl.setLightingArray()


def animate():
    while True:
        for i in range(len(ckl.outline)):
            ckl.outline[i].insert(0, ckl.outline[i].pop(-1))
        ckl.setLightingArray()
        sleep(0.1133)


animation = threading.Thread(target=animate, daemon=True)
animation.start()
