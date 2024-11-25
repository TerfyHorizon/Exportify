import os
import sys
import json
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import re
import tkinter as tk
from tkinter import filedialog, messagebox, simpledialog

def create_directories():
    """Create necessary directories in the user's Documents folder."""
    documents_path = os.path.join(os.path.expanduser("~"), "Documents")
    app_dir = os.path.join(documents_path, "Exportify-GUI")
    playlists_dir = os.path.join(app_dir, "Playlists")

    os.makedirs(playlists_dir, exist_ok=True)

    return app_dir, playlists_dir

def sanitize_filename(filename):
    """Remove or replace characters that are not allowed in file names."""
    return re.sub(r'[<>:"/\\|?*]', '-', filename)

def create_config_template(config_file):
    if not os.path.exists(config_file):
        config_template = {
            "_instructions": [
                "To use Exportify-GUI, you need to provide your Spotify API credentials.",
                "1. Go to https://developer.spotify.com/dashboard/applications",
                "2. Log in with your Spotify account.",
                "3. Click 'Create an App' and fill in the required details.",
                "4. After creating the app, you'll be given a 'Client ID' and 'Client Secret'.",
                "5. Copy and paste your Client ID and Client Secret into the fields below.",
                "6. Save the file and run Exportify again."
            ],
            "client_id": "YOUR_SPOTIFY_CLIENT_ID",
            "client_secret": "YOUR_SPOTIFY_CLIENT_SECRET"
        }
        with open(config_file, 'w') as f:
            json.dump(config_template, f, indent=4)

def create_readme(readme_file):
    if not os.path.exists(readme_file):
        readme_content = """\
Exportify-GUI - README

Exportify-GUI is a tool that allows you to export Spotify playlists to a text file.

Getting Started:
================
1. Obtain your Spotify API credentials:
   a. Go to https://developer.spotify.com/dashboard/applications
   b. Log in with your Spotify account.
   c. Click 'Create an App' and fill in the required details.
   d. After creating the app, you'll receive a 'Client ID' and 'Client Secret'.
   e. Copy and paste these into the 'config.json' file created by the tool.

2. Run Exportify-GUI:
   - On first run, Exportify-GUI will generate the 'config.json' file and create the necessary directories.
   - Edit this file to include your Spotify credentials.
   - Use the GUI to export Spotify playlists.

Usage:
======
1. Open the application.
2. Click the "Export Playlist" button.
3. Paste the Spotify playlist URL when prompted.

Notes:
======
- The playlist tracks will be saved to a text file named after the playlist in the 'Playlists' folder.
- Ensure you have an active internet connection when using Exportify-GUI.
"""
        with open(readme_file, 'w') as f:
            f.write(readme_content)

def authenticate_spotify(config_file):
    """Authenticate with Spotify using credentials from the config file."""
    with open(config_file, 'r') as f:
        config = json.load(f)
    client_credentials_manager = SpotifyClientCredentials(
        client_id=config['client_id'], 
        client_secret=config['client_secret']
    )
    sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)
    return sp

def save_tracks_to_file(sp, playlist_id, playlists_dir):
    """Save the tracks from a Spotify playlist to a text file."""
    playlist = sp.playlist(playlist_id)
    playlist_name = sanitize_filename(playlist['name'])
    track_list = []
    offset = 0
    limit = 100

    while True:
        response = sp.playlist_tracks(playlist_id, offset=offset, limit=limit)
        items = response['items']
        if not items:
            break
        
        for item in items:
            track = item['track']
            track_info = f"{track['name']} by {', '.join([artist['name'] for artist in track['artists']])}"
            track_list.append(track_info)
        
        offset += limit

    output_file = os.path.join(playlists_dir, f"{playlist_name}.txt")
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write("\n".join(track_list))
    
    return playlist_name, len(track_list), output_file

def on_export_click():
    """Handle the export button click in the GUI."""
    playlist_url = simpledialog.askstring(
        "Enter Playlist URL", 
        "Paste the Spotify Playlist URL:",
        parent=root
    )
    if not playlist_url:
        messagebox.showwarning("Input Error", "No playlist URL provided.")
        return
    
    try:
        playlist_id = playlist_url.split("/")[-1].split("?")[0]
        playlist_name, track_count, output_file = save_tracks_to_file(sp, playlist_id, playlists_dir)
        messagebox.showinfo("Export Successful", f"Playlist '{playlist_name}' exported successfully!\n"
                                                 f"Total tracks: {track_count}\n"
                                                 f"Saved to: {output_file}")
    except Exception as e:
        messagebox.showerror("Error", f"Failed to export playlist: {e}")

def setup_gui():
    """Setup the main GUI window."""
    root = tk.Tk()
    root.title("Exportify-GUI")
    root.geometry("500x350")
    root.resizable(False, False)
    root.configure(bg="#212121")

    tk.Label(root, text="Exportify-GUI", font=("Arial", 24), fg="white", bg="#212121").pack(pady=20)
    tk.Label(root, text="Export Spotify Playlists to Text Files", font=("Arial", 14), fg="white", bg="#212121").pack(pady=10)

    export_button = tk.Button(root, text="Export Playlist", command=on_export_click, width=20, height=2, font=("Arial", 12), bg="#424242", fg="white")
    export_button.pack(pady=30)

    tk.Label(root, text="Created by TerfyHorizon", font=("Arial", 10), fg="white", bg="#212121").pack(pady=10)
    return root

# Setup directories and authenticate Spotify
app_dir, playlists_dir = create_directories()
config_file = os.path.join(app_dir, "config.json")
readme_file = os.path.join(app_dir, "README.txt")

if not os.path.exists(config_file):
    create_config_template(config_file)

if not os.path.exists(readme_file):
    create_readme(readme_file)

try:
    sp = authenticate_spotify(config_file)
except Exception as e:
    messagebox.showerror("Authentication Error", f"Failed to authenticate with Spotify: {e}")
    sys.exit()

# Start the GUI
root = setup_gui()
root.mainloop()