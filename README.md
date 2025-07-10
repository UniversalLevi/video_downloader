# heheDownloader

heheDownloader is a beginner-friendly, fully automated command-line tool for downloading videos from almost any website, including YouTube, Facebook, Twitter, and more. It uses Python and yt-dlp under the hood, and automatically sets up everything you need—including ffmpeg for best quality downloads—so you can just paste a link and get your video in the highest quality available.

## Features
- Download videos from hundreds of sites (YouTube, Facebook, Twitter, etc.)
- Always gets the best available video and audio quality, merging them into a single MP4 file
- Fully automated: automatically installs Python dependencies and sets up ffmpeg if needed
- No manual setup required after cloning the project
- Works on Windows (auto-setup for ffmpeg), and can be adapted for Linux/macOS
- Simple, clean command-line interface
- Falls back to a single-file download if merging fails

## How to Use

### 1. Prerequisites
- Python 3.7 or higher must be installed on your system. You can download it from [python.org](https://www.python.org/downloads/).

### 2. Installation
1. Download or clone this repository to your computer.
2. Open a terminal (Command Prompt or PowerShell on Windows) and navigate to the project folder.
3. Install Python dependencies (the script will do this automatically if you skip this step):
   ```bash
   pip install -r requirements.txt
   ```

### 3. Download a Video
You can run the downloader in two ways:

#### Option 1: Interactive (recommended)
Just run:
```bash
python main.py
```
The script will prompt you to paste the video URL.

#### Option 2: Direct URL
You can also provide the video URL as a command-line argument:
```bash
python main.py <video_url>
```

### 4. What Happens Next?
- The script checks for yt-dlp and ffmpeg. If they are missing, it installs/sets them up automatically.
- ffmpeg is only downloaded once and reused for future downloads.
- The video will be downloaded in the best available quality and saved in the current directory with its original title.
- If merging fails, the script will automatically try to download the best single file available.

## Notes
- Only download content you have the rights to.
- For advanced options (batch downloads, format selection, etc.), you can modify the script to add more yt-dlp features.
- On Linux/macOS, you may need to install ffmpeg using your package manager (e.g., `sudo apt install ffmpeg` or `brew install ffmpeg`).

---

Enjoy your videos! If you have any issues or want more features, feel free to ask or contribute.