import subprocess
import sys
import os

# Ensure dependencies are installed
try:
    import yt_dlp
except ImportError:
    print("yt-dlp not found. Installing dependencies...")
    subprocess.check_call([sys.executable, '-m', 'pip', 'install', '-r', 'requirements.txt'])

# Get video URL from command line or prompt
if len(sys.argv) > 1:
    url = sys.argv[1]
else:
    url = input("Enter the video URL to download: ")

# Run downloader.py with the provided URL
subprocess.run([sys.executable, 'downloader.py', url]) 