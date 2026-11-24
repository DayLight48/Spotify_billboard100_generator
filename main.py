import requests
from bs4 import BeautifulSoup
import os
from dotenv import load_dotenv
import spotipy
from spotipy.oauth2 import SpotifyOAuth

load_dotenv()

date = "2026-02-21"
spotify_endpoint = "https://api.spotify.com/v1/me/playlists"

response = requests.get(f"https://appbrewery.github.io/bakeboard-hot-100/{date}/")
soup = BeautifulSoup(response.text,"html.parser")

all_songs = soup.find_all(name="h3", class_="chart-entry__title")

songs_names = [song.getText() for song in all_songs]
#print(songs_names)

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
    client_id=os.environ["CLIENT_ID_SPOTIFY"],
    client_secret=os.environ["CLIENT_SECRET_SPOTIFY"],
    redirect_uri="http://127.0.0.1:9090",
    scope="playlist-modify-private",
    show_dialog=True,
    cache_path="token.txt"
))

#results = sp.current_user_saved_tracks()

print("\nBuscando las canciones de la fecha ingresada....")
song_uris = []
year = date.split("-")[0]
for song in songs_names:
    result = sp.search(q=f"track:{song} year:{year}", type="track")
    try:
        uri = result["tracks"]["items"][0]["uri"]
        song_uris.append(uri)
    except IndexError:
        print(f"{song} doesn't exist in Spotify. Skipped.")
print(song_uris)

print("\n¡Busqueda terminada!")
print("\nCreando la playlist...")
result = sp.current_user_playlist_create(name=f"{date} Billboard 100", public=False)
print("\n¡La playlist fue creada exitosamente!")

sp.playlist_add_items(playlist_id=result["id"], items=song_uris)
print("\nLas canciones han sido añadidas exitosamente y todo esta listo para que pueda disfrutar :=)")
