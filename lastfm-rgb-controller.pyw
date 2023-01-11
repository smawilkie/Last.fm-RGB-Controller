from dotenv import load_dotenv
import os
from PIL import Image
from pystray import Icon, Menu, MenuItem
from time import sleep
import lastfm
import razer
import nzxt
import corsair

load_dotenv(".env")
width = int(os.getenv("KEYBOARD_WIDTH"))
height = int(os.getenv("KEYBOARD_HEIGHT"))


def exit():
    global exitCode
    exitCode = 1
    print("Set exit code to 1, exiting...")
    icon.stop()


if __name__ == "__main__":
    icon = Icon("Last.fm RGB Controller", title="Last.fm RGB Controller", icon=Image.open("icon.ico"), menu=Menu(MenuItem("Exit", exit)))
    exitCode = 0
    mostRecentURL = ""
    icon.run_detached()

    cycle = 0
    while exitCode == 0:
        url = lastfm.getAlbumArtURL("init" if cycle == 0 else None)
        if url is not None and url != mostRecentURL:
            mostRecentURL = url
            filename = lastfm.saveAlbumArt(url, width, height, 4)
            pixels = lastfm.showPixels(filename)
            razer.set(pixels, height, width)
            nzxt.set(pixels, "super-wave", "normal")
            corsair.set(pixels)

        cycle = 1
        sleep(0.5)
