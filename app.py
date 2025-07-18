from flask import Flask, request, send_file, jsonify
import yt_dlp, os, uuid

app = Flask(__name__)

@app.route('/download', methods=['POST'])
def download_video():
    url = request.json.get('url')
    if not url:
        return jsonify({"error": "No URL provided"}), 400

    try:
        file_id = str(uuid.uuid4())
        output_template = f"/tmp/{file_id}.%(ext)s"

        ydl_opts = {
            "outtmpl": output_template,
            "format": "bestvideo+bestaudio/best",
            "merge_output_format": "mp4",
            # optional but harmless for YouTube:
            "http_headers": {
                "User-Agent": (
                    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                    "AppleWebKit/537.36 (KHTML, like Gecko) "
                    "Chrome/122.0.0.0 Safari/537.36"
                ),
                "Accept-Language": "en-US,en;q=0.9",
            },
            # point to the *real* location of your exported cookies
            "cookiefile": "/opt/render/project/src/cookies.txt",
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            downloaded_path = ydl.prepare_filename(info).replace("%(ext)s", "mp4")

        return send_file(downloaded_path, as_attachment=True)

    except Exception as e:
        return jsonify({"error": str(e)}), 500
