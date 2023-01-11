from liquidctl import find_liquidctl_devices

devices = find_liquidctl_devices()

for device in devices:
    with device.connect():
        device.initialize()
        if "NZXT Smart Device" in device.description:
            lights = device


def setColours(colours, mode, speed):
    with lights.connect():
        lights.set_color(channel="led", mode=mode, colors=colours, speed=speed)
        


def set(pixels: list, mode: str="super-fixed", speed: str="normal"):
    colours = [pixels[0, 0], pixels[1, 0], pixels[3, 0], pixels[5, 0], pixels[7, 0], pixels[9, 0], pixels[11, 0], pixels[13, 0], pixels[15, 0], pixels[16, 0],
               pixels[4, 1], pixels[5, 1], pixels[6, 2], pixels[7, 2], pixels[8, 3], pixels[9, 3], pixels[10, 4], pixels[11, 4], pixels[12, 5], pixels[13, 5]]
    setColours(colours, mode, speed)
