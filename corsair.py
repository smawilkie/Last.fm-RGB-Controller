from cuesdk import CueSdk, CorsairDeviceFilter, CorsairDeviceType, CorsairError, CorsairLedColor
from time import sleep
import threading

sdk = CueSdk()
animationPaused = True

def on_state_changed(evt):
   print(evt.state)

err = sdk.connect(on_state_changed)
details, err = sdk.get_session_details()

devices, err = sdk.get_devices(CorsairDeviceFilter(device_type_mask=CorsairDeviceType.CDT_MemoryModule))
while err == CorsairError.CE_NotConnected:
   devices, err = sdk.get_devices(CorsairDeviceFilter(device_type_mask=CorsairDeviceType.CDT_MemoryModule))


def setColoursFromPixels(colours: list):
   global animationPaused
   animationPaused = True
   sdk.set_led_colors(devices[0].device_id, [CorsairLedColor(id+524289, pixel[0], pixel[1], pixel[2], 255) for id, pixel in enumerate(colours)])
   sleep(0.02)
   animationPaused = False


def set(pixels: list):
   colours = [pixels[2, 5], pixels[1, 5], pixels[1, 4], pixels[2, 3], pixels[1, 3], pixels[2, 2], pixels[1, 2], pixels[2, 1], pixels[2, 0], pixels[1, 0],
              pixels[6, 5], pixels[5, 5], pixels[5, 4], pixels[6, 3], pixels[5, 3], pixels[6, 2], pixels[5, 2], pixels[6, 1], pixels[6, 0], pixels[5, 0],
              pixels[10, 5], pixels[9, 5], pixels[9, 4], pixels[10, 3], pixels[9, 3], pixels[10, 2], pixels[9, 2], pixels[10, 1], pixels[10, 0], pixels[9, 0],
              pixels[14, 5], pixels[13, 5], pixels[13, 4], pixels[14, 3], pixels[13, 3], pixels[14, 2], pixels[13, 2], pixels[14, 1], pixels[14, 0], pixels[13, 0]]

   setColoursFromPixels(colours)


def animate():
   global animationPaused
   while True:
      if not animationPaused:
         currentColours = sdk.get_led_colors(devices[0].device_id, [CorsairLedColor(id, None, None, None, None) for id in range(524289, 524329)])[0]
         currentColours = [(colour.r, colour.g, colour.b, colour.a) for colour in currentColours]

         currentColours.insert(0, currentColours.pop())
         setColoursFromPixels(currentColours)
      sleep(0.05)


animation = threading.Thread(target=animate, daemon=True)
animation.start()
