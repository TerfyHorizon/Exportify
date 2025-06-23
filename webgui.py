# webgui.py
from flask import Flask, render_template, request
import threading
import webbrowser
from .exportify import authenticate_spotify, save_tracks, save_multiple_playlists
from .config import load_config

def run(host="127.0.0.1"):
    config = load_config()
    app = Flask(__name__)
    sp = authenticate_spotify(config)
    output_dir = config['output']['output_dir']
    port = config.get('webgui', {}).get('port', 5050)

    @app.route('/')
    def index():
        return render_template('index.html')

    @app.route('/export', methods=['POST'])
    def export():
        export_format = request.form['format']
        batch_file = request.files.get('batch_file')

        if batch_file and batch_file.filename:
            lines = batch_file.read().decode('utf-8').splitlines()
            playlist_urls = [line.strip() for line in lines if line.strip()]
            playlist_ids = [url.split('/')[-1].split('?')[0] for url in playlist_urls]
            try:
                results = save_multiple_playlists(sp, playlist_ids, output_dir, export_format)
                return render_template(
                    'result.html',
                    heading="Batch Export Successful",
                    results=results
                )
            except Exception as e:
                return render_template(
                    'result.html',
                    heading="Error",
                    playlist_name="N/A",
                    track_count="N/A",
                    output_file=str(e)
                )

        playlist_url = request.form.get('playlist_url', '')
        playlist_id = playlist_url.split('/')[-1].split('?')[0]

        try:
            playlist_name, track_count, output_file = save_tracks(
                sp, playlist_id, output_dir, export_format
            )
            return render_template(
                'result.html',
                heading="Export Successful",
                playlist_name=playlist_name,
                track_count=track_count,
                output_file=output_file
            )
        except Exception as e:
            return render_template(
                'result.html',
                heading="Error",
                playlist_name="N/A",
                track_count="N/A",
                output_file=str(e)
            )

    def open_browser():
        target = "127.0.0.1" if host in ("0.0.0.0", "") else host
        webbrowser.open(f"http://{target}:{port}")

    threading.Timer(1.0, open_browser).start()
    app.run(host=host, port=port, debug=False)
