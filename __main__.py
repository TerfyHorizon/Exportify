# __main__.py
import sys
import argparse

def main():
    parser = argparse.ArgumentParser(description="Exportify v3.3.0 - Spotify playlist exporter (WebGUI by default)")
    parser.add_argument('--cli', action='store_true', help="Run in CLI mode instead of WebGUI.")
    parser.add_argument('--playlist-url', type=str, help="Provide playlist URL directly (skips interactive CLI).")
    parser.add_argument('--output-dir', type=str, help="Custom output directory.")
    parser.add_argument('--format', type=str, help="Specify output format: markdown, txt, or csv.")
    parser.add_argument('--batch', type=str, help="Provide a file with playlist URLs to export in batch mode.")
    parser.add_argument('--bind', type=str, metavar='IP', help="Bind WebGUI to the specified IP address.")
    parser.add_argument('--allow-external', action='store_true', help="Acknowledge the risks of binding to a non-local IP.")

    
    args = parser.parse_args()

    host_ip = args.bind or "127.0.0.1"

    if args.bind and not args.allow_external and host_ip != "127.0.0.1":
        print(
            "WARNING: External hosting of ExportifyX WebGUI is NOT supported by the developer "
            "and may expose your machine to potential threats. Proceed at your own risk."
        )
        input("Press Enter to exit...")
        return

    if args.cli:
        from . import cli
        cli.run(args)
    else:
        from . import webgui
        webgui.run(host=host_ip)


if __name__ == "__main__":
    main()
