from flask import Flask, request, send_file, jsonify
import yt_dlp
import os
import uuid

app = Flask(__name__)

@app.route('/download', methods=['POST'])
def download_video():
    url = request.json.get('url')
    if not url:
        return jsonify({"error": "No URL provided"}), 400

    try:
        file_id = str(uuid.uuid4())
        output_template = f"/tmp/{file_id}.%(ext)s"  # <-- 💡 This was missing

        ydl_opts = {
            'outtmpl': output_template,
            'format': 'bestvideo+bestaudio/best',
            'merge_output_format': 'mp4',
            'extractor_args': {
                'generic': ['impersonate=firefox']
            }
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            downloaded_path = ydl.prepare_filename(info).replace("%(ext)s", "mp4")

        return send_file(downloaded_path, as_attachment=True)

    except Exception as e:
        return jsonify({"error": str(e)}), 500
