import sys
from yt_dlp import YoutubeDL

def download_video(url):
    ydl_opts = {
        'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best',
        'progress_hooks': [lambda d: print(f"Status: {d['status']} - {d.get('filename', '')}")],
        'outtmpl': '%(title)s.%(ext)s',
        'merge_output_format': 'mp4',
    }
    try:
        with YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
        print('Download completed!')
    except Exception as e:
        print(f'Error during merging or download: {e}\nFalling back to best single file (may be lower quality)...')
        # Fallback: best single file
        fallback_opts = {
            'format': 'best',
            'progress_hooks': [lambda d: print(f"Status: {d['status']} - {d.get('filename', '')}")],
            'outtmpl': '%(title)s.%(ext)s',
        }
        try:
            with YoutubeDL(fallback_opts) as ydl:
                ydl.download([url])
            print('Fallback download completed!')
        except Exception as e2:
            print(f'Fallback also failed: {e2}')

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python downloader.py <video_url>")
        sys.exit(1)
    download_video(sys.argv[1]) 