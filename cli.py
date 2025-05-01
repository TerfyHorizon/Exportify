# cli.py
import os
from .exportify import authenticate_spotify, save_tracks, save_multiple_playlists
from .config import load_config

def run(args):
    """Run Exportify in CLI mode."""
    config = load_config()
    sp = authenticate_spotify(config)

    # Determine output directory
    output_dir = args.output_dir or config['output']['output_dir']
    
    # Determine export format
    export_format = args.format or config.get('output', {}).get('default_format', 'markdown')

    if args.batch:
        if not os.path.exists(args.batch):
            print(f"ERROR: Batch file not found: {args.batch}")
            return
        with open(args.batch, 'r', encoding='utf-8') as f:
            playlist_urls = [line.strip() for line in f if line.strip()]
        playlist_ids = [parse_playlist_id(url) for url in playlist_urls]
        results = save_multiple_playlists(sp, playlist_ids, output_dir, export_format)
        print_export_results(results)
        return

    if args.playlist_url:
        # Non-interactive mode (user provided URL)
        playlist_ids = [parse_playlist_id(args.playlist_url)]
        results = save_multiple_playlists(sp, playlist_ids, output_dir, export_format)
        print_export_results(results)
    else:
        # Interactive mode
        batch_mode = input("Batch mode? (y/n): ").strip().lower() == 'y'
        if batch_mode:
            batch_file = input("Enter batch file path (e.g., batch_playlists.txt): ").strip()
            if not batch_file or not os.path.exists(batch_file):
                print("ERROR: Batch file not found. Exiting.")
                return
            with open(batch_file, 'r', encoding='utf-8') as f:
                playlist_urls = [line.strip() for line in f if line.strip()]
            playlist_ids = [parse_playlist_id(url) for url in playlist_urls]
            results = save_multiple_playlists(sp, playlist_ids, output_dir, export_format)
            print_export_results(results)
        else:
            playlist_url = input("Enter Spotify playlist URL: ").strip()
            if not playlist_url:
                print("ERROR: No URL provided. Exiting.")
                return
            playlist_id = parse_playlist_id(playlist_url)
            playlist_name, track_count, output_file = save_tracks(sp, playlist_id, output_dir, export_format)
            print("\nSUCCESS: Playlist '{}' exported successfully.".format(playlist_name))
            print("Total tracks: {}".format(track_count))
            print("Saved to: {}".format(output_file))


def parse_playlist_id(playlist_url):
    """Extract playlist ID from Spotify URL."""
    return playlist_url.split("/")[-1].split("?")[0]

def print_export_results(results):
    """Print batch export results."""
    for playlist_name, track_count, output_file in results:
        print("\nSUCCESS: Playlist '{}' exported.".format(playlist_name))
        print("Total tracks: {}".format(track_count))
        print("Saved to: {}".format(output_file))
