from cuesdk import CueSdk


def setColours(colours):
    global sdk
    sdk = CueSdk()

    connected = sdk.connect()
    if not connected:
        err = sdk.get_last_error()
        print("Handshake failed: %s" % err)
        return

    ids = list(range(600, 610))
    sticks = [sdk.get_led_colors_by_device_index(0, ids), sdk.get_led_colors_by_device_index(1, ids), sdk.get_led_colors_by_device_index(2, ids), sdk.get_led_colors_by_device_index(3, ids)]

    for id, stick in enumerate(sticks):
        for led, item in enumerate(stick):
            item.r = colours[(10*id) + led][0]
            item.g = colours[(10*id) + led][1]
            item.b = colours[(10*id) + led][2]
        sdk.set_led_colors_buffer_by_device_index(id, stick)

    sdk.set_led_colors_flush_buffer()

def set(pixels):
    colours = [pixels[1, 0], pixels[2, 0], pixels[2, 1], pixels[1, 2], pixels[2, 2], pixels[1, 3], pixels[2, 3], pixels[1, 4], pixels[1, 5], pixels[2, 5],
               pixels[5, 0], pixels[6, 0], pixels[6, 1], pixels[5, 2], pixels[6, 2], pixels[5, 3], pixels[6, 3], pixels[5, 4], pixels[5, 5], pixels[6, 5],
               pixels[9, 0], pixels[10, 0], pixels[10, 1], pixels[9, 2], pixels[10, 2], pixels[9, 3], pixels[10, 3], pixels[9, 4], pixels[9, 5], pixels[10, 5],
               pixels[13, 0], pixels[14, 0], pixels[14, 1], pixels[13, 2], pixels[14, 2], pixels[13, 3], pixels[14, 3], pixels[13, 4], pixels[13, 5], pixels[14, 5]]
    setColours(colours)
