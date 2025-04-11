import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import os

SPOTIPY_CLIENT_ID = os.environ.get("SPOTIPY_CLIENT_ID")
SPOTIPY_CLIENT_SECRET = os.environ.get("SPOTIPY_CLIENT_SECRET")

def get_spotify_tracks(playlist_url):
    sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(
        client_id=SPOTIPY_CLIENT_ID,
        client_secret=SPOTIPY_CLIENT_SECRET
    ))

    results = sp.playlist_tracks(playlist_url)
    tracks = []
    for item in results["items"]:
        track = item["track"]
        if track:
            tracks.append({
                "title": track["name"],
                "artist": track["artists"][0]["name"]
            })
    return tracks
