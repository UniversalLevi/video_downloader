# heheDownloader

A simple command-line tool to download videos from any supported website using yt-dlp.

## Installation

1. Install Python 3.7 or higher.
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

```bash
python main.py
```
- You can also provide a video URL as an argument:
  ```bash
  python main.py <video_url>
  ```

The video will be downloaded in the best available single file quality to the current directory with its original title.

## Notes
- Supports hundreds of sites (YouTube, Facebook, Twitter, etc.) via yt-dlp.
- Only download content you have the rights to.
- For advanced options, you can modify the script to add more yt-dlp features.
- This tool does not require ffmpeg and works out of the box, but will not merge separate video/audio streams (downloads the best single file available).