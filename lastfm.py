import io
import os
import requests
from dotenv import load_dotenv
from PIL import Image, ImageEnhance

load_dotenv(".env")
api_key = os.getenv("API_KEY")
user = os.getenv("LASTFM_USERNAME")

if not os.path.exists("img"):
    os.makedirs("img")


def getAlbumArtURL(mode: str = None) -> str:
    headers = {"user-agent": "Chroma for Last.fm"}
    url = "https://ws.audioscrobbler.com/2.0/"

    payload = {
        "method": "user.getrecenttracks",
        "user": user,
        "limit": "1",
        "api_key": api_key,
        "format": "json",
    }

    try:
        response = requests.get(url, headers=headers, params=payload)
        if response.json()['recenttracks']['@attr']['user'] != user:
            return None

        trackInfo = response.json()["recenttracks"]["track"][0]
        albumArtURL = trackInfo["image"][-1]["#text"]
        artist = trackInfo["artist"]["#text"]
        album = trackInfo["album"]["#text"]
        print("Checking Lastfm...")

        if mode == "init" or trackInfo.get("@attr").get("nowplaying") == "true":
            print(f"Listening to: {artist} - {album}")
            return albumArtURL
        else:
            return None
    except:
        pass


def saveAlbumArt(url: str, width: int, height: int, saturation: int = 1) -> str:
    filename = url.split("/")[-1]
    id = filename.split(".")[0]

    if not os.path.exists(f"img/{id}.png"):
        imageData = requests.get(url).content
        with Image.open(io.BytesIO(imageData)) as image:
            image = image.resize((width, height))
            image = image.convert("RGB")
            image = ImageEnhance.Color(image).enhance(saturation)
            image.save(f"img/{id}.png")

        print(f"New album, saved album art as img/{id}.png")

    return f"img/{id}.png"


def showPixels(filename: str) -> list:
    image = Image.open(filename)
    pixels = image.load()
    return pixels
