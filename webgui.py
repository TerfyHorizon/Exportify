# webgui.py
from flask import Flask, render_template, request
import threading
import webbrowser
from .exportify import authenticate_spotify, save_tracks
from .config import load_config

def run():
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
        playlist_url = request.form['playlist_url']
        export_format = request.form['format']
        playlist_id = playlist_url.split("/")[-1].split("?")[0]

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
        webbrowser.open(f"http://127.0.0.1:{port}")

    threading.Timer(1.0, open_browser).start()
    app.run(host="127.0.0.1", port=port, debug=False)
