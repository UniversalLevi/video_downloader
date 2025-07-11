from flask import Flask, request, jsonify, render_template_string
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

DARK_HTML = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>heheDownloader</title>
    <style>
        body {
            background: #181a1b;
            color: #f1f1f1;
            font-family: 'Segoe UI', Arial, sans-serif;
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            min-height: 100vh;
            margin: 0;
        }
        .container {
            background: #23272a;
            padding: 2rem 2.5rem;
            border-radius: 1rem;
            box-shadow: 0 4px 32px #000a;
            max-width: 400px;
            width: 100%;
        }
        h1 {
            margin-bottom: 1.5rem;
            font-size: 2rem;
            text-align: center;
            color: #00bfae;
        }
        input[type="text"] {
            width: 100%;
            padding: 0.75rem;
            border-radius: 0.5rem;
            border: none;
            margin-bottom: 1rem;
            font-size: 1rem;
            background: #181a1b;
            color: #f1f1f1;
        }
        button {
            width: 100%;
            padding: 0.75rem;
            border-radius: 0.5rem;
            border: none;
            background: #00bfae;
            color: #181a1b;
            font-size: 1.1rem;
            font-weight: bold;
            cursor: pointer;
            transition: background 0.2s;
        }
        button:hover {
            background: #009e8e;
        }
        .result {
            margin-top: 1.5rem;
            padding: 1rem;
            border-radius: 0.5rem;
            background: #22262a;
            color: #f1f1f1;
            word-break: break-all;
            text-align: center;
        }
        .spinner {
            margin: 1rem auto 0 auto;
            border: 4px solid #23272a;
            border-top: 4px solid #00bfae;
            border-radius: 50%;
            width: 32px;
            height: 32px;
            animation: spin 1s linear infinite;
        }
        @keyframes spin {
            0% { transform: rotate(0deg); }
            100% { transform: rotate(360deg); }
        }
        a.download-link {
            color: #00bfae;
            text-decoration: underline;
            word-break: break-all;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>heheDownloader</h1>
        <form id="downloadForm">
            <input type="text" id="url" name="url" placeholder="Paste video URL here..." required />
            <button type="submit">Download</button>
        </form>
        <div id="spinner" class="spinner" style="display:none;"></div>
        <div id="result" class="result" style="display:none;"></div>
    </div>
    <script>
        const form = document.getElementById('downloadForm');
        const resultDiv = document.getElementById('result');
        const spinner = document.getElementById('spinner');
        form.addEventListener('submit', async (e) => {
            e.preventDefault();
            resultDiv.style.display = 'none';
            spinner.style.display = 'block';
            const url = document.getElementById('url').value;
            try {
                const res = await fetch('/download', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ url })
                });
                const data = await res.json();
                spinner.style.display = 'none';
                resultDiv.style.display = 'block';
                if (data.status === 'success') {
                    resultDiv.innerHTML = `✅ Downloaded: <span class='download-link'>${data.filename}</span><br>Check the server's download folder.`;
                } else {
                    resultDiv.innerHTML = `❌ Error: ${data.error || 'Unknown error.'}`;
                }
            } catch (err) {
                spinner.style.display = 'none';
                resultDiv.style.display = 'block';
                resultDiv.innerHTML = `❌ Error: ${err.message}`;
            }
        });
    </script>
</body>
</html>
'''

@app.route('/', methods=['GET'])
def index():
    return render_template_string(DARK_HTML)

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

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000) 