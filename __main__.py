# __main__.py
import sys
import argparse

def main():
    parser = argparse.ArgumentParser(description="Exportify v3.2 - Spotify playlist exporter (WebGUI by default)")
    parser.add_argument('--cli', action='store_true', help="Run in CLI mode instead of WebGUI.")
    parser.add_argument('--playlist-url', type=str, help="Provide playlist URL directly (skips interactive CLI).")
    parser.add_argument('--output-dir', type=str, help="Custom output directory.")
    parser.add_argument('--format', type=str, help="Specify output format: markdown, txt, or csv.")
    parser.add_argument('--batch', type=str, help="Provide a file with playlist URLs to export in batch mode.")

    
    args = parser.parse_args()

    if args.cli:
        from . import cli
        cli.run(args)
    else:
        from . import webgui
        webgui.run()


if __name__ == "__main__":
    main()
