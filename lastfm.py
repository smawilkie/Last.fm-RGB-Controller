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


class AlbumInfo:
    def __init__(self, artist, album, artURL):
        self.artist = artist
        self.album = album
        self.artURL = artURL


def getAlbumInfo(mostRecentURL: str, mode: str = None) -> str:
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

        if mode == "init" or trackInfo.get("@attr").get("nowplaying") == "true" or albumArtURL != mostRecentURL:
            print(f"Listening to: {artist} - {album}")
            return AlbumInfo(artist, album, albumArtURL)
        else:
            return None
    except:
        pass


def saveAlbumArt(info: AlbumInfo, width: int, height: int, saturation: int = 1) -> str:
    for illegalSymbol in ["*", ".", "\"", "/", "\\", "[", "]", ":", ";", "|", ","]:
        info.artist = info.artist.replace(illegalSymbol, "")
        info.album = info.album.replace(illegalSymbol, "")

    if not os.path.exists(f"img/{info.artist} - {info.album}") and info.artURL is not None:
        imageData = requests.get(info.artURL).content

        if len(imageData) == 0:
            print("Album art download failed")
            return None

        os.makedirs(f"img/{info.artist} - {info.album}")

        with Image.open(io.BytesIO(imageData)) as image:
            keyboardImage = image.resize((width, height)).convert("RGB")
            keyboardImage = ImageEnhance.Color(keyboardImage).enhance(saturation)
            keyboardImage.save(f"img/{info.artist} - {info.album}/{width}x{height}.png")

            caseLEDImage = image.resize((10, 10)).convert("RGB")
            caseLEDImage = ImageEnhance.Color(caseLEDImage).enhance(saturation)
            caseLEDImage.save(f"img/{info.artist} - {info.album}/10x10.png")

        print(f"New album, saved album art in img/{info.artist} - {info.album}")

    return f"img/{info.artist} - {info.album}"
