from json import load
from os import getenv
import threading
from time import sleep
from requests import Session, post

class CKL:
    def __init__(self):
        corePropsPath = getenv('PROGRAMDATA') + "\SteelSeries\SteelSeries Engine 3\coreProps.json" 
        self.sseAddress = f'http://{load(open(corePropsPath))["address"]}'
        self.game = 'CUSTOM_KEYBOARD_LIGHTING'
        self.game_display_name = 'Custom Keyboard Lighting'
        self.event = 'BITMAP_EVENT'

        self.bitmap = [[0,0,0] for i in range(132)]

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
        
    def getGameDisplayName(self):
        """Returns the name displayed in SteelSeries Engine for this application."""
        return self.game_display_name

    def registerGame(self):
        """Registers this application to Engine."""
        endpoint = f'{self.sseAddress}/game_metadata'
        payload = {
            "game" : self.game,
            "game_display_name" : self.game_display_name,
            "developer" : "yrfriendmark"
        }
        post(endpoint, json=payload)

    def removeGame(self):
        """Removes this application from Engine."""
        endpoint = f'{self.sseAddress}/remove_game'
        payload = {
            "game": self.game
        }
        post(endpoint, json=payload)

    def removeGameEvent(self):
        """Removes a lighting event from Engine."""
        endpoint = f'{self.sseAddress}/remove_game_event'
        payload = {
            "game": self.game,
            "event" : self.event
        }
        post(endpoint, json=payload)

    def sendHeartbeat(self):
        """Sends an empty lighting event to Engine to prevent timeout."""
        endpoint = f'{self.sseAddress}/game_heartbeat'
        payload = {
                "game": self.game
        }
        post(endpoint, json=payload)

    def sendGameEvent(self, args):
        """Sends a lighting event/frame to Engine."""
        endpoint = f'{self.sseAddress}/game_event'
        frame = [[0, 0, 0] for i in range(132)]
        payload = {
            "game": self.game,
            "event": self.event,
            "data" : {
                "value" : 100,
                "frame" : {
                    "bitmap" : frame
                }
            }
        }

        with Session() as s:
            for key in self.keys:
                print(key)
                frame[key] = [0, 255, 0]
                s.post(endpoint, json=payload)
                sleep(0.01)

    def setLightingArray(self):
        endpoint = f'{self.sseAddress}/game_event'
        frame = [[0, 0, 0] for i in range(132)]

        usedColours = [self.outline[0][0], self.outline[0][1], self.outline[0][2], self.outline[0][3], self.outline[0][4], self.outline[0][5], self.outline[0][6], self.outline[0][7], self.outline[0][8], self.outline[0][9], self.outline[0][10], self.outline[0][11], self.outline[0][12], self.outline[0][13],
                       self.outline[1][0], self.outline[1][1], self.outline[1][2], self.outline[1][3], self.outline[1][4], self.outline[1][5], self.outline[1][6], self.outline[1][7], self.outline[1][8], self.outline[1][9], self.outline[1][10], self.outline[1][11], self.outline[1][12], self.outline[1][13], self.outline[1][14],
                       self.outline[2][0], self.outline[2][1], self.outline[2][2], self.outline[2][3], self.outline[2][4], self.outline[2][5], self.outline[2][6], self.outline[2][7], self.outline[2][8], self.outline[2][9], self.outline[2][10], self.outline[2][11], self.outline[2][12], self.outline[2][13], self.outline[2][14],
                       self.outline[3][0], self.outline[3][1], self.outline[3][2], self.outline[3][3], self.outline[3][4], self.outline[3][5], self.outline[3][6], self.outline[3][7], self.outline[3][8], self.outline[3][9], self.outline[3][10], self.outline[3][11], self.outline[3][13], self.outline[3][14],
                       self.outline[4][0], self.outline[4][1], self.outline[4][2], self.outline[4][3], self.outline[4][4], self.outline[4][5], self.outline[4][6], self.outline[4][7], self.outline[4][8], self.outline[4][9], self.outline[4][10], self.outline[4][11], self.outline[4][13], self.outline[4][14],
                       self.outline[5][0], self.outline[5][1], self.outline[5][2], self.outline[5][5], self.outline[5][6], self.outline[5][7], self.outline[5][8], self.outline[5][9], self.outline[5][12], self.outline[5][13], self.outline[5][14]]
               
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

def set(pixels: list):
    colours = []
    for y in range(6):
        currentRow = []
        for x in range(17):
            if x != 1 and x != 15:
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
