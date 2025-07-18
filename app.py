from flask import Flask, request, send_file
import yt_dlp
import os
import uuid

app = Flask(__name__)

@app.route('/download', methods=['POST'])
def download_video():
    url = request.json.get('url')
    if not url:
        return {"error": "No URL provided"}, 400

    file_id = str(uuid.uuid4())
    output_path = f"./downloads/{file_id}.%(ext)s"

    ydl_opts = {
        'outtmpl': output_path,
        'format': 'bestvideo+bestaudio/best',
        'merge_output_format': 'mp4',
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=True)
        downloaded_file = ydl.prepare_filename(info).replace('%(ext)s', 'mp4')

    return send_file(downloaded_file, as_attachment=True)

if __name__ == '__main__':
    os.makedirs('./downloads', exist_ok=True)
    app.run(debug=True)
