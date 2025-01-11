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
FFMPEG_LOCATION = os.getenv("FFMPEG_LOCATION", "ffmpeg")

# Konfiguracja Spotify API
spotify = Spotify(auth_manager=SpotifyClientCredentials(
    client_id=SPOTIFY_CLIENT_ID,
    client_secret=SPOTIFY_CLIENT_SECRET
))

def get_spotify_tracks(playlist_url):
    """Pobiera tytuły utworów z playlisty Spotify."""
    playlist_id = playlist_url.split("/")[-1].split("?")[0]
    results = spotify.playlist_items(playlist_id)
    return [f"{item['track']['name']} {item['track']['artists'][0]['name']}" for item in results['items']]

def download_content(urls, output_dir="downloads", search=False, is_playlist=False):
    """Uniwersalna funkcja do pobierania treści z YouTube i wyszukiwania utworów."""
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
        'ffmpeg_location': FFMPEG_LOCATION,
        'default_search': 'ytsearch' if search else None,
        'noplaylist': not is_playlist,
        'http_headers': {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
    }
    with YoutubeDL(ydl_opts) as ydl:
        try:
            print(f"Pobieranie: {urls}")
            ydl.download(urls if isinstance(urls, list) else [urls])
        except Exception as e:
            print(f"Nie udało się pobrać: {urls}. Błąd: {e}")

def is_spotify_url(url):
    return "spotify.com" in url

def is_youtube_url(url):
    return "youtube.com" in url or "youtu.be" in url

if __name__ == "__main__":
    url = input("Podaj URL playlisty lub utworu (Spotify/YouTube): ").strip()
    output_dir = "downloads"

    if is_spotify_url(url):
        print("Wykryto URL Spotify. Pobieranie...")
        tracks = get_spotify_tracks(url)
        download_content(tracks, output_dir, search=True)
    elif is_youtube_url(url):
        if "list=" in url:
            print("Wykryto playlistę YouTube. Pobieranie...")
            download_content(url, output_dir, is_playlist=True)
        else:
            print("Wykryto wideo YouTube. Pobieranie...")
            download_content(url, output_dir)
    else:
        print("Nieobsługiwany URL. Podaj link do Spotify lub YouTube.")
