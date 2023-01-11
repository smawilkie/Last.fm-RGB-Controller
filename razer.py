from ChromaPython import ChromaApp, ChromaAppInfo, ChromaGrid
from time import sleep

Info = ChromaAppInfo()
Info.DeveloperName = "Sam Wilkie"
Info.DeveloperContact = "sam.wilkie2903@gmail.com"
Info.Category = "application"
Info.SupportedDevices = ["keyboard", "mouse"]
Info.Description = "Last.fm -> Chroma integration."
Info.Title = "Last.fm RGB Controller"
App = ChromaApp(Info)
sleep(1)


def set(pixels: list, height: int, width: int):
    keyboardGrid = ChromaGrid("Keyboard")
    mouseGrid = ChromaGrid("Mouse")
    chromaLinkGrid = ChromaGrid("ChromaLink")

    for x in range(0, height):
        for y in range(0, width):
            keyboardGrid[x][y+1].set(*pixels[y,x])

    mouseGrid[2][3].set(*pixels[8, 0])
    mouseGrid[7][3].set(*pixels[8, 5])

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
