# app.py
from flask import Flask, request, render_template, jsonify
from pytube import YouTube
import os

app = Flask(__name__, static_url_path='/static')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/get_video_info', methods=['POST'])
def get_video_info():
    url = request.json['url']
    try:
        yt = YouTube(url)
        streams = yt.streams.filter(file_extension="mp4").order_by('resolution').desc()
        available_streams = [{'itag': stream.itag, 'resolution': stream.resolution, 'mime_type': stream.mime_type} for stream in streams]
        return jsonify({'title': yt.title, 'streams': available_streams})
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@app.route('/download_video', methods=['POST'])
def download_video():
    url = request.json['url']
    try:
        yt = YouTube(url)
        stream_1080p = yt.streams.filter(res="1080p", file_extension="mp4").first()
        stream_720p = yt.streams.filter(res="720p", file_extension="mp4").first()

        if stream_1080p:
            stream = stream_1080p
        elif stream_720p:
            stream = stream_720p
        else:
            return jsonify({'error': 'Neither 1080p nor 720p streams are available.'}), 400

        download_path = os.path.expanduser('~/Downloads')
        stream.download(download_path)
        return jsonify({'message': 'Download completed!', 'path': download_path})
    except Exception as e:
        return jsonify({'error': str(e)}), 400

if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
