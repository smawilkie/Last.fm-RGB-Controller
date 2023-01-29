from cuesdk import CueSdk, CorsairDeviceFilter, CorsairDeviceType, CorsairError, CorsairLedColor
from time import sleep
import threading
from PIL import Image

global paused
paused = True

sdk = CueSdk()

def on_state_changed(evt):
   print(evt.state)

err = sdk.connect(on_state_changed)
details, err = sdk.get_session_details()

devices, err = sdk.get_devices(CorsairDeviceFilter(device_type_mask=CorsairDeviceType.CDT_MemoryModule))
while err == CorsairError.CE_NotConnected:
   devices, err = sdk.get_devices(CorsairDeviceFilter(device_type_mask=CorsairDeviceType.CDT_MemoryModule))


def setColoursFromPixels(colours: list):
   sdk.set_led_colors(devices[0].device_id, [CorsairLedColor(id+524289, pixel[0], pixel[1], pixel[2], 255) for id, pixel in enumerate(colours)])
   sleep(0.02)


def set(filename: str):
   global paused
   paused = True
   pixels = Image.open(f"{filename}/10x10.png").load()
   colours = [pixels[i, j] for i in [0, 4, 7, 9] for j in range(9, -1, -1)]

   setColoursFromPixels(colours)
   paused = False
   

def animate(pattern: int):
   while True:
      currentColours = sdk.get_led_colors(devices[0].device_id, [CorsairLedColor(id, None, None, None, None) for id in range(524289, 524329)])[0]
      currentColours = [(colour.r, colour.g, colour.b, colour.a) for colour in currentColours]

      match pattern:
         case 1:  # pattern 1: move lights between sticks individually
            currentColours.insert(0, currentColours.pop())

         case 2:  # pattern 2: rows move
            newLights = []
            for i in range(4):
               newLights.append(currentColours[10*i:10*i+10])
            for i in range(len(newLights)):
               newLights[i].append(newLights[i].pop(0))

            currentColours = [j for sub in newLights for j in sub]

         case 3:  # pattern 3: columns move
            currentColours = currentColours[30:] + currentColours[0:31]

      if not paused:
         setColoursFromPixels(currentColours)
      sleep(0.05)


animation = threading.Thread(target=animate, args=(2,), daemon=True)
animation.start()
