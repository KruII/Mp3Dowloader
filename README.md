# MediaDownloader

MediaDownloader is a Python-based tool to download Spotify tracks, Spotify playlists, YouTube videos, and YouTube playlists. It allows users to fetch content and convert it into MP3 format seamlessly.

## Features
- Download individual Spotify tracks by searching on YouTube.
- Download Spotify playlists and convert all tracks to MP3.
- Download individual YouTube videos or entire playlists.
- Detects URLs automatically and handles them appropriately.
- Configurable through a `.env` file.

## Requirements
- **Python version:** Tested on Python 3.13.1
- **Dependencies:**
  - `yt-dlp` (for downloading YouTube content)
  - `spotipy` (for Spotify API interactions)
  - `python-dotenv` (for environment variable management)

## Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/your-username/MediaDownloader.git
   cd MediaDownloader
   ```
2. Install the required Python libraries:
   ```bash
   pip install yt-dlp spotipy python-dotenv
   ```

3. Install FFmpeg:
   - **Windows:** Download from [FFmpeg Official Website](https://ffmpeg.org/download.html) and add it to your system PATH.
   - **Linux/macOS:** Install via package manager:
     ```bash
     sudo apt install ffmpeg  # For Debian/Ubuntu
     brew install ffmpeg      # For macOS
     ```

## Configuration
1. Create a `.env` file in the project directory with the following content:
   ```env
   SPOTIFY_CLIENT_ID=your_spotify_client_id
   SPOTIFY_CLIENT_SECRET=your_spotify_client_secret
   FFMPEG_LOCATION=/path/to/ffmpeg  # Optional if FFmpeg is in PATH
   ```
2. Replace `your_spotify_client_id` and `your_spotify_client_secret` with credentials from your Spotify Developer account. You can create an app and get credentials from [Spotify for Developers](https://developer.spotify.com/dashboard/applications).

## Usage
Run the script using Python:
```bash
python media_downloader.py
```

### Commands
- Enter a **Spotify** or **YouTube URL** (track, playlist, video, or playlist).
- Use the following commands to exit:
  - `exit`
  - `quit`
  - `q`
  - `stop`

### Supported URLs
- **Spotify**:
  - Track: `https://open.spotify.com/track/track_id`
  - Playlist: `https://open.spotify.com/playlist/playlist_id`
- **YouTube**:
  - Video: `https://youtu.be/video_id` or `https://youtube.com/watch?v=video_id`
  - Playlist: `https://youtube.com/playlist?list=playlist_id`

## Example
1. Download a Spotify track:
   ```bash
   Enter arguments: https://open.spotify.com/track/track_id
   ```

2. Download a Spotify playlist:
   ```bash
   Enter arguments: https://open.spotify.com/playlist/playlist_id
   ```

3. Download a YouTube video:
   ```bash
   Enter arguments: https://youtu.be/video_id
   ```

4. Download a YouTube playlist:
   ```bash
   Enter arguments: https://youtube.com/playlist?list=playlist_id
   ```

5. Exit the application:
   ```bash
   Enter arguments: quit
   ```

## License
This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Contribution
Feel free to open issues or submit pull requests for improvements or bug fixes.

## Disclaimer
This tool is intended for personal use. Ensure you have the rights to download and use the content.

