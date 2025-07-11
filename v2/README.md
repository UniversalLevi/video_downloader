# v2: Web Frontend/API

This is the user-facing web service. It provides a modern UI and API for users to submit video URLs. It sends download requests to v1 (the backend bridge) and streams the result to the user.

- Accepts user input via web form or API.
- Forwards requests to v1's /bridge-download endpoint.
- Handles download streaming and user feedback.

## Deployment

1. **Set Environment Variables:**
   - `V1_URL`: The URL of your v1 backend (e.g., `https://hehedownload.up.railway.app/bridge-download`)
   - `BRIDGE_SECRET`: The shared secret you set for v1

2. **Dependencies:**
   - Python 3.7+
   - All dependencies in `requirements.txt` (Flask, requests)

3. **Start Command:**
   ```sh
   python app.py
   ```

4. **Access the UI:**
   - Visit the root URL in your browser to use the downloader.

---

## Security
- The frontend never exposes the secret to users; it is only used for backend communication.
- v1 must be secured with the same secret. 