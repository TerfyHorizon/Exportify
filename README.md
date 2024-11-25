# Exportify

**Exportify** is a Python-based tool that allows you to export Spotify playlists to text files using a simple graphical user interface (GUI). This application is ideal for anyone who wants to save their playlists as text files for reference, sharing, or backup.

---

## Features

- **Graphical User Interface (GUI):** No need to use the command line.
- **Spotify Playlist Export:** Export your playlists to text files, including the track name and artist.
- **Dark Theme:** Minimalist dark theme with an aesthetic `#212121` background.
- **Automatic Setup:** Automatically creates necessary directories and config files on first run.

---

## Getting Started

### Prerequisites

1. **Spotify API Credentials**
   - Go to the [Spotify Developer Dashboard](https://developer.spotify.com/dashboard/applications).
   - Log in with your Spotify account.
   - Click **Create an App** and provide the required details.
   - Copy the **Client ID** and **Client Secret**.

2. **Python (Optional for Developers)**
   - [Download Python](https://www.python.org/) (if you want to customize or run the script directly).

### Installation

1. **Download the Executable**
   - Download the latest release of `exportify-gui.exe` from the [Releases](https://github.com/TerfyHorizon/Exportify/releases) page.

2. **Run the Application**
   - Double-click `exportify-gui.exe`.
   - The application will create the following directories in your `Documents` folder:
     ```
     Documents/
       └── Exportify-GUI/
           ├── Playlists/
           ├── exportify_config.json
           └── README.txt
     ```

3. **Set Up API Credentials**
   - Open the `exportify_config.json` file in a text editor.
   - Paste your **Client ID** and **Client Secret** into the respective fields:
     ```json
     {
         "client_id": "YOUR_SPOTIFY_CLIENT_ID",
         "client_secret": "YOUR_SPOTIFY_CLIENT_SECRET"
     }
     ```

4. **Start Exporting Playlists**
   - Launch `exportify-gui.exe`.
   - Click the **Export Playlist** button.
   - Paste your Spotify playlist URL when prompted.
   - The exported playlist will be saved as a `.txt` file in the `Playlists` folder.

---

## Usage

### Exporting a Playlist

1. Copy the URL of a Spotify playlist (e.g., `https://open.spotify.com/playlist/5ZQsZWjg49ke0IvsmcuAQB`).
2. Open the application and click **Export Playlist**.
3. Paste the URL into the dialog box.
4. The playlist will be exported as a `.txt` file in `Documents/Exportify-GUI/Playlists`.

---

## Example Output

If you export a playlist named "My Playlist," the `.txt` file will look like this:

```
Song 1 by Artist A
Song 2 by Artist B
Song 3 by Artist C
...
```

---

## Development

If you'd like to modify the script or contribute, follow these steps:

### Prerequisites

- Python 3.9+
- Install dependencies:
  ```bash
  pip install spotipy
  ```

### Running the Script

1. Clone the repository:
   ```bash
   git clone https://github.com/your-repo/exportify-gui.git
   cd exportify-gui
   ```

2. Run the script:
   ```bash
   python ExportifyGUI.py
   ```

### Building the Executable

To create a standalone executable, use [PyInstaller](https://pyinstaller.org/):
```bash
pyinstaller --onefile --name exportify-gui ExportifyGUI.py
```

The executable will be created in the `dist` directory.

---

## Known Issues

1. **Cache Warnings:**
   - Cache-related warnings (`Couldn't write token to cache`) may appear but do not affect functionality.

2. **Rate Limits:**
   - Spotify's API enforces rate limits. If you're exporting a very large playlist, the process may temporarily pause.

---

## Contributing

Contributions are welcome! Please fork the repository and submit a pull request.

---

## License

This project is licensed under the MIT License. See the `LICENSE` file for details.

---

## Acknowledgments

- [Spotify Developer API](https://developer.spotify.com/documentation/web-api/)
- [Spotipy Library](https://spotipy.readthedocs.io/en/2.16.1/)

---

**Enjoy Exporting Your Playlists with Exportify-GUI!**
