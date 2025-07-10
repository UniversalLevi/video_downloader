import sys
from yt_dlp import YoutubeDL

def download_video(url):
    ydl_opts = {
        'format': 'bestvideo+bestaudio/best',  # Always get best quality
        'progress_hooks': [lambda d: print(f"Status: {d['status']} - {d.get('filename', '')}")],
        'outtmpl': '%(title)s.%(ext)s',
        'merge_output_format': 'mp4',  # Ensure merged output is mp4 if possible
    }
    try:
        with YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
        print('Download completed!')
    except Exception as e:
        print(f'Error: {e}')

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python downloader.py <video_url>")
        sys.exit(1)
    download_video(sys.argv[1]) 