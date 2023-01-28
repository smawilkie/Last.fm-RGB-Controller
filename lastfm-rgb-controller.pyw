from dotenv import load_dotenv
import os, socket
from PIL import Image
from pystray import Icon, Menu, MenuItem
from time import sleep
import lastfm
import razer

if socket.gethostname() == "Sam-W-PC":
    import nzxt
    import corsair

if socket.gethostname() == "MSI":
    import steelseries

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
        sleep(0.5)

        albumInfo = lastfm.getAlbumInfo(mostRecentURL, "init" if cycle == 0 else None)

        if albumInfo is None:
            continue

        if albumInfo.artURL == mostRecentURL:
            continue

        mostRecentURL = albumInfo.artURL
        filename = lastfm.saveAlbumArt(albumInfo, width, height, 4)

        razer.set(filename, height, width)

        if socket.gethostname() == "Sam-W-PC":
            nzxt.set(filename, "super-wave", "slower")
            corsair.set(filename)

        if socket.gethostname() == "MSI":
            steelseries.set(filename)

        cycle = 1
