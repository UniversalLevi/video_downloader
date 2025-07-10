import subprocess
import sys
import os
import platform
import zipfile
import urllib.request
from shutil import which

# Ensure dependencies are installed
try:
    import yt_dlp
except ImportError:
    print("yt-dlp not found. Installing dependencies...")
    subprocess.check_call([sys.executable, '-m', 'pip', 'install', '-r', 'requirements.txt'])

# Function to show download progress

def download_progress_hook(count, block_size, total_size):
    percent = int(count * block_size * 100 / (total_size + 1))
    sys.stdout.write(f"\rDownloading ffmpeg... {percent}%")
    sys.stdout.flush()
    if percent >= 100:
        print("\nExtracting ffmpeg...")

# Function to download and extract ffmpeg for Windows
FFMPEG_URL = "https://www.gyan.dev/ffmpeg/builds/ffmpeg-release-essentials.zip"
FFMPEG_ZIP = "ffmpeg-release-essentials.zip"
FFMPEG_DIR = "ffmpeg-bin"

def setup_ffmpeg_windows():
    print("Starting ffmpeg download...")
    urllib.request.urlretrieve(FFMPEG_URL, FFMPEG_ZIP, reporthook=download_progress_hook)
    with zipfile.ZipFile(FFMPEG_ZIP, 'r') as zip_ref:
        zip_ref.extractall(FFMPEG_DIR)
    # Find the bin directory
    for root, dirs, files in os.walk(FFMPEG_DIR):
        if 'ffmpeg.exe' in files:
            bin_path = root
            os.environ['PATH'] = bin_path + os.pathsep + os.environ['PATH']
            print(f"ffmpeg is set up at {bin_path}")
            return True
    print("Failed to set up ffmpeg.")
    return False

# Check if ffmpeg is available, if not, try to set it up
if which('ffmpeg') is None:
    if platform.system() == 'Windows':
        if not setup_ffmpeg_windows():
            print("Error: Could not set up ffmpeg automatically. Please install it manually.")
            sys.exit(1)
    else:
        print("Error: ffmpeg is not installed. Please install it using your package manager (e.g., sudo apt install ffmpeg or brew install ffmpeg).")
        sys.exit(1)

# Get video URL from command line or prompt
if len(sys.argv) > 1:
    url = sys.argv[1]
else:
    url = input("Enter the video URL to download: ")

# Run downloader.py with the provided URL
subprocess.run([sys.executable, 'downloader.py', url]) 