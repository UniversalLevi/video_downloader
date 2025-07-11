from flask import Flask, request, render_template_string, send_file, Response
import requests
import os
import tempfile

# Use the deployed v1 backend URL
V1_URL = os.environ.get("V1_URL", "https://hehedownload.up.railway.app/bridge-download")
BRIDGE_SECRET = os.environ.get("BRIDGE_SECRET", "supersecret")

app = Flask(__name__)

DARK_HTML = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>heheDownloader v2</title>
    <style>
        body { background: #181a1b; color: #f1f1f1; font-family: 'Segoe UI', Arial, sans-serif; display: flex; flex-direction: column; align-items: center; justify-content: center; min-height: 100vh; margin: 0; }
        .container { background: #23272a; padding: 2rem 2.5rem; border-radius: 1rem; box-shadow: 0 4px 32px #000a; max-width: 400px; width: 100%; }
        h1 { margin-bottom: 1.5rem; font-size: 2rem; text-align: center; color: #00bfae; }
        input[type="text"], textarea { width: 100%; padding: 0.75rem; border-radius: 0.5rem; border: none; margin-bottom: 1rem; font-size: 1rem; background: #181a1b; color: #f1f1f1; }
        button { width: 100%; padding: 0.75rem; border-radius: 0.5rem; border: none; background: #00bfae; color: #181a1b; font-size: 1.1rem; font-weight: bold; cursor: pointer; transition: background 0.2s; }
        button:hover { background: #009e8e; }
        .result { margin-top: 1.5rem; padding: 1rem; border-radius: 0.5rem; background: #22262a; color: #f1f1f1; word-break: break-all; text-align: center; }
        .spinner { margin: 1rem auto 0 auto; border: 4px solid #23272a; border-top: 4px solid #00bfae; border-radius: 50%; width: 32px; height: 32px; animation: spin 1s linear infinite; }
        @keyframes spin { 0% { transform: rotate(0deg); } 100% { transform: rotate(360deg); } }
        a.download-link { color: #00bfae; text-decoration: underline; word-break: break-all; }
        label { font-size: 0.95rem; color: #b0b0b0; }
    </style>
</head>
<body>
    <div class="container">
        <h1>heheDownloader</h1>
        <form id="downloadForm" method="POST" enctype="multipart/form-data">
            <input type="text" id="url" name="url" placeholder="Paste video URL here..." required />
            <label for="cookies">(Optional) Paste cookies.txt here for private/restricted videos:</label>
            <textarea id="cookies" name="cookies" rows="3" placeholder="Paste cookies.txt here..."></textarea>
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
            const cookies = document.getElementById('cookies').value;
            const formData = new FormData();
            formData.append('url', url);
            formData.append('cookies', cookies);
            fetch('/', { method: 'POST', body: formData })
                .then(async response => {
                    spinner.style.display = 'none';
                    if (response.headers.get('Content-Disposition')) {
                        // File download
                        const blob = await response.blob();
                        const filename = response.headers.get('Content-Disposition').split('filename=')[1].replace(/"/g, '');
                        const link = document.createElement('a');
                        link.href = window.URL.createObjectURL(blob);
                        link.download = filename;
                        document.body.appendChild(link);
                        link.click();
                        document.body.removeChild(link);
                        resultDiv.style.display = 'block';
                        resultDiv.innerHTML = `✅ Download started: <span class='download-link'>${filename}</span>`;
                    } else {
                        const data = await response.json();
                        resultDiv.style.display = 'block';
                        resultDiv.innerHTML = `❌ Error: ${data.error || 'Unknown error.'}`;
                    }
                })
                .catch(err => {
                    spinner.style.display = 'none';
                    resultDiv.style.display = 'block';
                    resultDiv.innerHTML = `❌ Error: ${err.message}`;
                });
        });
    </script>
</body>
</html>
'''

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'GET':
        return render_template_string(DARK_HTML)
    url = request.form.get('url')
    cookies = request.form.get('cookies')
    if not url:
        return render_template_string(DARK_HTML + "<script>document.getElementById('result').innerHTML='❌ Error: URL required.';document.getElementById('result').style.display='block';</script>")
    payload = {"url": url}
    if cookies:
        payload["cookies"] = cookies
    headers = {"x-bridge-secret": BRIDGE_SECRET}
    try:
        with requests.post(V1_URL, json=payload, headers=headers, stream=True, timeout=600) as r:
            if r.status_code == 200 and 'Content-Disposition' in r.headers:
                filename = r.headers.get('Content-Disposition').split('filename=')[1].replace('"', '')
                temp = tempfile.NamedTemporaryFile(delete=False)
                for chunk in r.iter_content(chunk_size=8192):
                    temp.write(chunk)
                temp.close()
                return send_file(temp.name, as_attachment=True, download_name=filename)
            else:
                error = r.json().get('error', 'Unknown error.')
                return render_template_string(DARK_HTML + f"<script>document.getElementById('result').innerHTML='❌ Error: {error}';document.getElementById('result').style.display='block';</script>")
    except Exception as e:
        return render_template_string(DARK_HTML + f"<script>document.getElementById('result').innerHTML='❌ Error: {str(e)}';document.getElementById('result').style.display='block';</script>") 