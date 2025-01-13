import os
from yt_dlp import YoutubeDL
from spotipy.oauth2 import SpotifyClientCredentials
from spotipy import Spotify
from dotenv import load_dotenv

class MediaDownloader:
    """
    A class for handling downloading of Spotify tracks/playlists and YouTube videos/playlists.
    """
    def __init__(self):
        # Load environment variables
        load_dotenv()
        self.spotify_client_id = os.getenv("SPOTIFY_CLIENT_ID")
        self.spotify_client_secret = os.getenv("SPOTIFY_CLIENT_SECRET")
        self.ffmpeg_location = os.getenv("FFMPEG_LOCATION", "ffmpeg")
        self.output_dir = "downloads"

        # Initialize Spotify client
        self.spotify = Spotify(auth_manager=SpotifyClientCredentials(
            client_id=self.spotify_client_id,
            client_secret=self.spotify_client_secret
        ))

    def get_spotify_track(self, track_url):
        """
        Fetches the title and artist of a single Spotify track.
        
        Args:
            track_url (str): URL of the Spotify track.
        
        Returns:
            str: Formatted string with track title and artist.
        """
        track_id = track_url.split("/")[-1].split("?")[0]
        track = self.spotify.track(track_id)
        return f"{track['name']} {track['artists'][0]['name']}"

    def get_spotify_playlist(self, playlist_url):
        """
        Fetches all track titles and artists from a Spotify playlist.
        
        Args:
            playlist_url (str): URL of the Spotify playlist.
        
        Returns:
            list: List of formatted strings containing track titles and artists.
        """
        playlist_id = playlist_url.split("/")[-1].split("?")[0]
        results = self.spotify.playlist_items(playlist_id)
        return [f"{item['track']['name']} {item['track']['artists'][0]['name']}" for item in results['items']]

    def download_content(self, urls, search=False, is_playlist=False):
        """
        Downloads content from YouTube or searches for it on YouTube.
        
        Args:
            urls (str or list): Single URL or list of URLs to download or search for.
            search (bool): If True, performs a YouTube search for the query.
            is_playlist (bool): If True, treats the URL as a playlist.
        """
        os.makedirs(self.output_dir, exist_ok=True)
        ydl_opts = {
            'format': 'bestaudio/best',
            'outtmpl': f'{self.output_dir}/%(title)s.%(ext)s',
            'quiet': False,
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
            'ffmpeg_location': self.ffmpeg_location,
            'default_search': 'ytsearch' if search else None,
            'noplaylist': not is_playlist,
            'http_headers': {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
            }
        }
        with YoutubeDL(ydl_opts) as ydl:
            try:
                print(f"Downloading: {urls}")
                ydl.download(urls if isinstance(urls, list) else [urls])
            except Exception as e:
                print(f"Failed to download: {urls}. Error: {e}")

    def is_spotify_track_url(self, url):
        """Checks if the URL is for a Spotify track."""
        return "open.spotify.com/track" in url

    def is_spotify_playlist_url(self, url):
        """Checks if the URL is for a Spotify playlist."""
        return "open.spotify.com/playlist" in url

    def is_youtube_url(self, url):
        """Checks if the URL is for YouTube content."""
        return "youtube.com" in url or "youtu.be" in url

    def handle_url(self, url):
        """
        Handles the input URL and determines the appropriate action (Spotify or YouTube).
        
        Args:
            url (str): The URL to process.
        """
        if self.is_spotify_track_url(url):
            print("Detected Spotify track. Downloading...")
            track = self.get_spotify_track(url)
            self.download_content(track, search=True)
        elif self.is_spotify_playlist_url(url):
            print("Detected Spotify playlist. Downloading...")
            tracks = self.get_spotify_playlist(url)
            self.download_content(tracks, search=True)
        elif self.is_youtube_url(url):
            if "list=" in url:
                print("Detected YouTube playlist. Downloading...")
                self.download_content(url, is_playlist=True)
            else:
                print("Detected YouTube video. Downloading...")
                self.download_content(url)
        else:
            print("Unsupported URL. Please provide a Spotify or YouTube link.")

if __name__ == "__main__":
    # Create an instance of MediaDownloader
    downloader = MediaDownloader()

    # Define a list of exit commands
    exit_commands = {"exit", "quit", "q", "stop"}

    while True:
        # Get first URL input from the user
        url = next(arg for arg in input("Enter arguments: ").split() if arg.strip())

        # Check if the user wants to exit
        if url.lower() in exit_commands:
            break

        # Process the URL
        downloader.handle_url(url)

