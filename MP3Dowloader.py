import os
from yt_dlp import YoutubeDL
from spotipy.oauth2 import SpotifyClientCredentials
from spotipy import Spotify
from dotenv import load_dotenv

# Wczytaj zmienne z pliku .env
load_dotenv()

# Pobierz dane z .env
SPOTIFY_CLIENT_ID = os.getenv("SPOTIFY_CLIENT_ID")
SPOTIFY_CLIENT_SECRET = os.getenv("SPOTIFY_CLIENT_SECRET")
FFMPEG_LOCATION = os.getenv("FFMPEG_LOCATION")

# Konfiguracja Spotify API
spotify = Spotify(auth_manager=SpotifyClientCredentials(
    client_id=SPOTIFY_CLIENT_ID,
    client_secret=SPOTIFY_CLIENT_SECRET
))

def get_spotify_playlist_tracks(playlist_url):
    """Pobiera tytuły utworów z playlisty Spotify."""
    playlist_id = playlist_url.split("/")[-1].split("?")[0]
    results = spotify.playlist_items(playlist_id)
    tracks = []
    for item in results['items']:
        track = item['track']
        track_name = track['name']
        artist_name = track['artists'][0]['name']
        tracks.append(f"{track_name} {artist_name}")
    return tracks

def search_and_download_youtube(query, output_dir="downloads"):
    """Wyszukiwanie i pobieranie wideo/audio z YouTube za pomocą yt-dlp."""
    os.makedirs(output_dir, exist_ok=True)
    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': f'{output_dir}/%(title)s.%(ext)s',
        'quiet': False,
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
        'ffmpeg_location': 'C:/ffmpeg/bin',
        'noplaylist': True,
        'default_search': 'ytsearch',
        'max_downloads': 1,  # Pobieramy tylko pierwszy wynik
    }
    with YoutubeDL(ydl_opts) as ydl:
        try:
            print(f"Wyszukiwanie i pobieranie: {query}")
            ydl.download([query])
        except Exception as e:
            print(f"Nie udało się pobrać: {query}. Błąd: {e}")

def download_spotify_playlist(playlist_url, output_dir="downloads"):
    """Pobieranie playlisty Spotify za pomocą wyszukiwania i pobierania z YouTube."""
    tracks = get_spotify_playlist_tracks(playlist_url)
    for track in tracks:
        search_and_download_youtube(track, output_dir)

if __name__ == "__main__":
    spotify_playlist_url = input("Podaj URL playlisty Spotify: ")
    download_spotify_playlist(spotify_playlist_url)
