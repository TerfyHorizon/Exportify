import os
import sys
import json
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import re

def create_directories():
    """Create necessary directories in the user's Documents folder."""
    documents_path = os.path.join(os.path.expanduser("~"), "Documents")
    app_dir = os.path.join(documents_path, "Exportify")
    playlists_dir = os.path.join(app_dir, "Playlists")

    os.makedirs(playlists_dir, exist_ok=True)

    print(f"Directories have been created or verified:\n{app_dir}\n{playlists_dir}")
    return app_dir, playlists_dir

def get_app_file_path(app_dir, file_name):
    """Get the absolute path to a file in the application's directory."""
    return os.path.join(app_dir, file_name)

def sanitize_filename(filename):
    """Remove or replace characters that are not allowed in file names."""
    return re.sub(r'[<>:"/\\|?*]', '-', filename)

def create_config_template(config_file):
    if not os.path.exists(config_file):
        print("Creating config template...")
        config_template = {
            "_instructions": [
                "To use Exportify, you need to provide your Spotify API credentials.",
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
        try:
            with open(config_file, 'w') as f:
                json.dump(config_template, f, indent=4)
            print(f"Template created at: {config_file}")
        except Exception as e:
            print(f"Failed to create config template: {e}")
    else:
        print(f"Config template already exists at: {config_file}")

def create_readme(readme_file):
    if not os.path.exists(readme_file):
        print("Creating README...")
        readme_content = """\
Exportify - README

Exportify is a tool that allows you to export Spotify playlists to a text file.

Getting Started:
================
1. Obtain your Spotify API credentials:
   a. Go to https://developer.spotify.com/dashboard/applications
   b. Log in with your Spotify account.
   c. Click 'Create an App' and fill in the required details.
   d. After creating the app, you'll receive a 'Client ID' and 'Client Secret'.
   e. Copy and paste these into the 'exportify_config.json' file created by the tool.

2. Run Exportify:
   - On first run (double-click), Exportify will generate the 'exportify_config.json' file and create the necessary directories.
   - Edit this file to include your Spotify credentials.
   - After setup, run Exportify from the command line with the Spotify playlist URL to export the playlist.

Usage:
======
   Exportify.exe <Spotify Playlist URL>

Example:
========
   Exportify.exe https://open.spotify.com/playlist/5ZQsZWjg49ke0IvsmcuAQB

Modes of Operation:
===================
1. **Double-Click Setup Mode**:
   - If you double-click `Exportify.exe` (without providing any command-line arguments), it will perform the initial setup.
   - This includes creating necessary directories in your Documents folder (`Documents/Exportify` and `Documents/Exportify/Playlists`), and generating the `exportify_config.json` and `README.txt` files if they don't exist.

2. **Command-Line Export Mode**:
   - Once setup is complete, run `Exportify.exe` from the command line with a Spotify playlist URL to export the playlist.
   - The playlist's tracks will be saved to a text file in the `Documents/Exportify/Playlists` directory.

Notes:
======
- The playlist tracks will be saved to a text file named after the playlist.
- Ensure that you have an active internet connection when using Exportify.
- Cache Warnings: You may see cache-related warnings like "Couldn't read/write token to cache." These warnings are normal and do not affect the functionality of Exportify.

Adding Exportify to PATH (Optional):
====================================
Adding Exportify.exe to your system's PATH allows you to run Exportify from any command prompt without needing to navigate to its directory.

1. Locate the Directory of Exportify.exe:
   - Find the folder where Exportify.exe is located (e.g., C:\\Users\\YourUsername\\Documents\\Exportify\\dist).
   - Copy the full directory path.

2. Open System Properties:
   - Right-click the Start Menu and select "System".
   - Click "Advanced system settings" on the right side to open the System Properties window.

3. Edit the Environment Variables:
   - In the System Properties window, click the "Environment Variables" button.
   - Under "System variables", find and select the Path variable, then click "Edit".

4. Add the Directory to PATH:
   - In the Edit Environment Variable window, click "New".
   - Paste the directory path you copied earlier.
   - Click "OK" to close each window.

5. Verify the Addition:
   - Open a new command prompt (important to refresh the environment variables).
   - Type "Exportify" and press Enter. If it’s been added to PATH correctly, it should run without needing to specify the full path.

Once added, you can run Exportify from any command prompt by simply typing "Exportify".
"""
        try:
            with open(readme_file, 'w') as f:
                f.write(readme_content)
            print(f"README created at: {readme_file}")
        except Exception as e:
            print(f"Failed to create README: {e}")
    else:
        print(f"README already exists at: {readme_file}")

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
        print(f"Failed to authenticate with Spotify: {e}")
        input("Press Enter to exit...")
        sys.exit()

def extract_playlist_id(playlist_url):
    """Extract the playlist ID from the Spotify URL."""
    try:
        return playlist_url.split("/")[-1].split("?")[0]
    except Exception as e:
        print(f"Failed to extract playlist ID: {e}")
        input("Press Enter to exit...")
        sys.exit()

def save_tracks_to_file(sp, playlist_id, playlists_dir):
    """Save the tracks from a Spotify playlist to a text file, handling pagination."""
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
        
        print(f"Playlist '{playlist_name}' has been saved to {output_file}")
        print(f"Total number of tracks exported: {len(track_list)}")
    except Exception as e:
        print(f"Failed to save tracks to file: {e}")
        input("Press Enter to exit...")
        sys.exit()

def main():
    # Check if the script was run with a command-line argument
    if len(sys.argv) > 1:
        # Command-line usage (export playlist)
        playlist_url = sys.argv[1]

        # Use the user's Documents folder for saving output
        documents_path = os.path.join(os.path.expanduser("~"), "Documents")
        playlists_dir = os.path.join(documents_path, "Exportify", "Playlists")

        # Authenticate with Spotify
        config_file = os.path.join(documents_path, "Exportify", "exportify_config.json")
        sp = authenticate_spotify(config_file)

        # Extract playlist ID and save tracks to file
        playlist_id = extract_playlist_id(playlist_url)
        save_tracks_to_file(sp, playlist_id, playlists_dir)
        
        print("\nThe Spotify playlist has been successfully exported.")
    
    else:
        # No command-line argument provided, assume double-click and set up directories
        app_dir, playlists_dir = create_directories()

        # Define paths for config and README
        config_file = get_app_file_path(app_dir, 'exportify_config.json')
        readme_file = get_app_file_path(app_dir, 'README.txt')
        
        # Create config template and README file if they don't exist
        create_config_template(config_file)
        create_readme(readme_file)
        
        print("\nSetup complete. Please run the program from the command line with a Spotify playlist URL.")
        print("Example usage:\nExportify.exe https://open.spotify.com/playlist/5ZQsZWjg49ke0IvsmcuAQB")
    
    # Pause to keep the terminal open
    input("\nPress Enter to exit...")

if __name__ == '__main__':
    main()