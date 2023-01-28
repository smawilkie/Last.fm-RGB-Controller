from liquidctl import find_liquidctl_devices
from PIL import Image

devices = find_liquidctl_devices()

for device in devices:
    with device.connect():
        device.initialize()
        if "NZXT Smart Device" in device.description:
            lights = device


def setColours(colours, mode, speed):
    with lights.connect():
        lights.set_color(channel="led", mode=mode, colors=colours, speed=speed)
        

def set(filename: str, mode: str="super-fixed", speed: str="normal"):
    pixels = Image.open(f"{filename}/10x10.png").load()
    colours = [pixels[i, 0] for i in range(0, 10)] + [pixels[5, i] for i in range(0, 10)]
    setColours(colours, mode, speed)
