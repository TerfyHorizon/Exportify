# exportify.py
import os
import re
import csv
import json
import spotipy
from tqdm import tqdm
from spotipy.oauth2 import SpotifyClientCredentials

def sanitize_filename(filename):
    """Remove or replace characters that are not allowed in file names."""
    return re.sub(r'[<>:"/\\|?*]', '-', filename)

def authenticate_spotify(config):
    """Authenticate with Spotify using credentials from the config dictionary."""
    client_id = config['spotify']['client_id']
    client_secret = config['spotify']['client_secret']
    
    client_credentials_manager = SpotifyClientCredentials(
        client_id=client_id,
        client_secret=client_secret
    )
    sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)
    return sp

def save_tracks(sp, playlist_id, playlists_dir, output_format="markdown"):
    """Save the tracks from a Spotify playlist in the chosen output format."""
    playlist = sp.playlist(playlist_id)
    playlist_name = sanitize_filename(playlist['name'])
    tracks = []
    offset = 0
    limit = 100

    while True:
        response = sp.playlist_tracks(playlist_id, offset=offset, limit=limit)
        items = response['items']
        if not items:
            break

        for item in items:
            track = item['track']
            if track:  # Make sure it's not None
                track_name = track['name']
                artist_names = ', '.join([artist['name'] for artist in track['artists']])
                album_name = track['album']['name']
                tracks.append((track_name, artist_names, album_name))
        
        offset += limit

    os.makedirs(playlists_dir, exist_ok=True)

    output_file = os.path.join(playlists_dir, f"{playlist_name}.{_get_extension(output_format)}")
    
    # Export based on format
    if output_format == "markdown":
        _export_markdown(output_file, playlist_name, tracks)
    elif output_format == "txt":
        _export_txt(output_file, tracks)
    elif output_format == "csv":
        _export_csv(output_file, tracks)
    elif output_format == "json":
        _export_json(output_file, tracks)
    else:
        raise ValueError(f"Unsupported export format: {output_format}")
    
    return playlist_name, len(tracks), output_file

def _get_extension(format_name):
    """Helper to get file extension based on format."""
    if format_name == "markdown":
        return "md"
    elif format_name == "txt":
        return "txt"
    elif format_name == "csv":
        return "csv"
    elif format_name == "json":
        return "json"
    else:
        return "txt"  # Fallback safe

def _export_markdown(file_path, playlist_name, tracks):
    """Export tracks to Markdown file."""
    lines = [f"## {playlist_name}", "---"]
    for track_name, artist_names, _ in tracks:
        lines.append(f"- **{track_name}** : *{artist_names}*")
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write("\n".join(lines))

def _export_txt(file_path, tracks):
    """Export tracks to plain TXT."""
    lines = [f"{track_name} - {artist_names}" for track_name, artist_names, _ in tracks]
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write("\n".join(lines))

def _export_csv(file_path, tracks):
    """Export tracks to CSV."""
    with open(file_path, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(["Track Name", "Artist(s)", "Album Name"])
        for track_name, artist_names, album_name in tracks:
            writer.writerow([track_name, artist_names, album_name])

def _export_json(file_path, tracks):
    """Export tracks to JSON file."""
    data = []
    for track_name, artist_names, album_name in tracks:
        data.append({
            "track_name": track_name,
            "artist_names": artist_names.split(", "),
            "album_name": album_name
        })
    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2)

def save_multiple_playlists(sp, playlist_ids, playlists_dir, output_format="markdown"):
    results = []
    for playlist_id in tqdm(playlist_ids, desc="Exporting playlists", unit="playlist"):
        result = save_tracks(sp, playlist_id, playlists_dir, output_format)
        results.append(result)
    return results

