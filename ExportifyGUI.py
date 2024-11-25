import os
import sys
import json
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import re
import tkinter as tk
from tkinter import messagebox, simpledialog

def sanitize_filename(filename):
    """Remove or replace characters that are not allowed in file names."""
    return re.sub(r'[<>:"/\\|?*]', '-', filename)

def authenticate_spotify(config_file):
    """Authenticate with Spotify using credentials from the config file."""
    try:
        with open(config_file, 'r') as f:
            config = json.load(f)
        client_credentials_manager = SpotifyClientCredentials(
            client_id=config['client_id'], 
            client_secret=config['client_secret']
        )
        sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)
        return sp
    except Exception as e:
        messagebox.showerror("Authentication Error", f"Failed to authenticate with Spotify: {e}")
        sys.exit()

def save_tracks_to_file(sp, playlist_id, playlists_dir):
    """Save the tracks from a Spotify playlist to a text file."""
    try:
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
    except Exception as e:
        messagebox.showerror("Error", f"Failed to save tracks to file: {e}")
        sys.exit()

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

# Set up directories
script_dir = os.path.dirname(os.path.abspath(sys.argv[0]))
playlists_dir = os.path.join(script_dir, "Playlists")
config_file = os.path.join(script_dir, "config.json")

# Ensure Playlists directory exists
os.makedirs(playlists_dir, exist_ok=True)

# Authenticate with Spotify
sp = authenticate_spotify(config_file)

# Start the GUI
root = setup_gui()
root.mainloop()