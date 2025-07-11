from flask import Flask, request, jsonify
from yt_dlp import YoutubeDL
import logging
import os

app = Flask(__name__)

# Configure logging
logging.basicConfig(level=logging.INFO)

# Download directory
DOWNLOAD_DIR = os.environ.get('DOWNLOAD_DIR', '.')

# yt-dlp options for best quality
YDL_OPTS = {
    'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best',
    'outtmpl': os.path.join(DOWNLOAD_DIR, '%(title)s.%(ext)s'),
    'merge_output_format': 'mp4',
    'quiet': True,
    'no_warnings': True,
}

@app.route('/download', methods=['POST'])
def download():
    data = request.get_json(force=True, silent=True)
    if not data or 'url' not in data:
        return jsonify({'error': 'Missing "url" in request body'}), 400
    url = data['url']
    if not isinstance(url, str) or not url.strip():
        return jsonify({'error': 'Invalid URL'}), 400
    logging.info(f"Received download request for URL: {url}")
    try:
        with YoutubeDL(YDL_OPTS) as ydl:
            info = ydl.extract_info(url, download=True)
            filename = ydl.prepare_filename(info)
        logging.info(f"Download completed: {filename}")
        return jsonify({'status': 'success', 'filename': os.path.basename(filename)}), 200
    except Exception as e:
        logging.error(f"Download failed: {e}")
        return jsonify({'status': 'error', 'error': str(e)}), 500

@app.route('/')
def index():
    return jsonify({'message': 'Video Downloader API. POST to /download with {"url": "..."}.'}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000) 