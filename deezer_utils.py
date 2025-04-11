import requests

def get_deezer_tracks(playlist_url):
    playlist_id = playlist_url.strip('/').split('/')[-1].split('?')[0]
    api_url = f"https://api.deezer.com/playlist/{playlist_id}"
    res = requests.get(api_url).json()
    tracks = []
    for track in res.get("tracks", {}).get("data", []):
        tracks.append({
            "title": track["title"],
            "artist": track["artist"]["name"]
        })
    return tracks
