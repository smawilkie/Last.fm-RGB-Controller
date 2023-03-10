from ChromaPython import ChromaApp, ChromaAppInfo, ChromaGrid
from time import sleep
import threading
from PIL import Image

Info = ChromaAppInfo()
Info.DeveloperName = "Sam Wilkie"
Info.DeveloperContact = "sam.wilkie2903@gmail.com"
Info.Category = "application"
Info.SupportedDevices = ["keyboard", "mouse"]
Info.Description = "Last.fm -> Chroma integration."
Info.Title = "Last.fm RGB Controller"
App = ChromaApp(Info)
sleep(1)


def set(filename: str, height: int, width: int):
    pixels = Image.open(f"{filename}/{width}x{height}.png").load()

    keyboardGrid = ChromaGrid("Keyboard")
    mouseGrid = ChromaGrid("Mouse")
    chromaLinkGrid = ChromaGrid("ChromaLink")

    for x in range(0, height):
        for y in range(0, width):
            keyboardGrid[x][y+1].set(*pixels[y,x])

    mouseGrid[2][3].set(*pixels[16, 2])
    mouseGrid[7][3].set(*pixels[16, 5])

    chromaLinkGrid[1].set(*pixels[1, 1])  # 1 = logo/top left (wraith prism)
    chromaLinkGrid[2].set(*pixels[8, 2])  # 2 = innner circle
    chromaLinkGrid[3].set(*pixels[16, 2])  # 3 = up/right
    chromaLinkGrid[4].set(*pixels[0, 2])  # 4 = down/left

    App.Keyboard.setCustomGrid(keyboardGrid)
    App.Keyboard.applyGrid()
    App.Mouse.setCustomGrid(mouseGrid)
    App.Mouse.applyGrid()
    App.ChromaLink.setCustomGrid(chromaLinkGrid)
    App.ChromaLink.applyGrid()


def animate(pattern: int):
    keyboardGrid = ChromaGrid("Keyboard")
    while True:
        lights = []
        for row in App.Keyboard._ColorGrid:
            currentRow = []
            for key in row:
                currentRow.append(key.getRGB())
            lights.append(currentRow)
        
        match pattern:
            case 1:  # pattern 1: move key lights between rows individually
                for index, row in enumerate(lights):
                    lights[index].insert(1, lights[index-1][-5])
                for index, row in enumerate(lights):
                    lights[index].pop(-5)

            case 2:  # pattern 2: rows move
                lights.insert(0, lights.pop(-1))

            case 3:  # pattern 3: columns move
                for i in range(len(lights)):
                    lights[i].insert(1, lights[i].pop(-5))

        for x in range(0, 6):
            for y in range(0, 22):
                keyboardGrid[x][y].set(*lights[x][y])

        App.Keyboard.setCustomGrid(keyboardGrid)
        App.Keyboard.applyGrid()

        mouseGrid = ChromaGrid("Mouse")
        mouseGrid[2][3].set(*lights[2][16])
        mouseGrid[7][3].set(*lights[5][16])
        App.Mouse.setCustomGrid(mouseGrid)
        App.Mouse.applyGrid()
            
        sleep(0.1)


animation = threading.Thread(target=animate, args=(3,), daemon=True)
animation.start()
