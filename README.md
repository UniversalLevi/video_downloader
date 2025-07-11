# heheDownloader (Web API Edition)

heheDownloader is a production-ready, fully automated web API for downloading videos from almost any website, including YouTube, Facebook, Twitter, and more. It uses Python, Flask, and yt-dlp, and is designed for easy deployment on cloud platforms like Render.

## Features
- Download videos from hundreds of sites (YouTube, Facebook, Twitter, etc.)
- Always gets the best available video and audio quality, merging them into a single MP4 file
- Fully automated: automatically installs Python dependencies and sets up ffmpeg if needed (on Windows)
- Simple, robust REST API for integration with other services or frontends
- Production-level error handling and logging

## How to Use

### 1. Prerequisites
- Python 3.7 or higher must be installed on your system (for local use)
- For cloud deployment (e.g., Render), just push your code and requirements.txt

### 2. Installation (Local)
1. Clone this repository:
   ```bash
   git clone <your-repo-url>
   cd heheDownloader
   ```
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. (Optional, Windows only) ffmpeg will be set up automatically if not found.

### 3. Running the API
```bash
python app.py
```
- The API will be available at `http://localhost:10000/`

### 4. Downloading a Video (API Usage)
Send a POST request to `/download` with a JSON body containing the video URL:

**Example using curl:**
```bash
curl -X POST http://localhost:10000/download \
     -H "Content-Type: application/json" \
     -d '{"url": "https://www.youtube.com/watch?v=YOUR_VIDEO_ID"}'
```

**Response:**
- On success: `{ "status": "success", "filename": "DownloadedFile.mp4" }`
- On error: `{ "status": "error", "error": "..." }`

### 5. Deploying to Render or Other Cloud
- Set your start command to `python app.py`.
- The API will listen on port 10000 by default (changeable in `app.py`).
- No interactive input is required; all requests are handled via HTTP.

## Notes
- Only download content you have the rights to.
- For advanced options (batch downloads, format selection, etc.), you can modify the API or yt-dlp options in `app.py`.
- On Linux/macOS, you may need to install ffmpeg using your package manager (e.g., `sudo apt install ffmpeg` or `brew install ffmpeg`).

---

Enjoy your videos! If you have any issues or want more features, feel free to ask or contribute.