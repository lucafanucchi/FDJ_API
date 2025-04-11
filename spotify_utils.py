# spotify_utils.py
import streamlit as st
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

def get_spotify_tracks(playlist_url):
    try:
        SPOTIPY_CLIENT_ID = st.secrets["spotify"]["CLIENT_ID"]
        SPOTIPY_CLIENT_SECRET = st.secrets["spotify"]["CLIENT_SECRET"]
    except KeyError:
        st.error("Credenciais do Spotify não configuradas corretamente no secrets.toml.")
        return []

    auth_manager = SpotifyClientCredentials(
        client_id=SPOTIPY_CLIENT_ID,
        client_secret=SPOTIPY_CLIENT_SECRET
    )
    sp = spotipy.Spotify(auth_manager=auth_manager)

    results = sp.playlist_items(playlist_url)
    tracks = []

    for item in results.get('items', []):
        track = item.get('track')
        if track:
            tracks.append({
                "title": track.get("name"),
                "artist": track.get("artists", [{}])[0].get("name", "")
            })

    return tracks