# Exportify (V-1.0)

**Exportify** is a command-line tool that allows you to export Spotify playlists to text files. This version of Exportify focuses on a streamlined, no-frills approach for users comfortable with the command line.

---

## Features

- **Command-Line Interface (CLI):** Simple and efficient, designed for users who prefer working with the terminal.
- **Spotify Playlist Export:** Export playlists as `.txt` files, including track names and artist names.
- **Automatic Directory Management:** Creates necessary directories and config files in your `Documents` folder on first run.

---

## Getting Started

### Prerequisites

1. **Spotify API Credentials**
   - Go to the [Spotify Developer Dashboard](https://developer.spotify.com/dashboard/applications).
   - Log in with your Spotify account.
   - Click **Create an App** and fill in the required details.
   - Copy the **Client ID** and **Client Secret**.

2. **Python (Required)**
   - Install Python 3.9+ from [python.org](https://www.python.org/).
   - Install the required dependencies:
     ```bash
     pip install spotipy
     ```

---

### Installation

1. **Clone the Repository**
   ```bash
   git clone https://github.com/TerfyHorizon/Exportify.git
   cd exportify
   ```

2. **Run the Script**
   ```bash
   python Exportify.py <Spotify Playlist URL>
   ```

3. **Set Up API Credentials**
   - On first run, the script generates the following files and directories in your `Documents` folder:
     ```
     Documents/
       └── Exportify/
           ├── Playlists/
           ├── exportify_config.json
           └── README.txt
     ```
   - Open `config.json` and paste your **Client ID** and **Client Secret**:
     ```json
     {
         "client_id": "YOUR_SPOTIFY_CLIENT_ID",
         "client_secret": "YOUR_SPOTIFY_CLIENT_SECRET"
     }
     ```

---

## Usage

To export a Spotify playlist:

1. Copy the playlist URL (e.g., `https://open.spotify.com/playlist/5ZQsZWjg49ke0IvsmcuAQB`).
2. Run the script:
   ```bash
   python Exportify.py <Spotify Playlist URL>
   ```
3. The playlist will be exported as a `.txt` file in `Documents/Exportify/Playlists`.

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

## Known Issues

1. **Cache Warnings**:
   - Cache-related warnings (`Couldn't write token to cache`) may appear but do not affect functionality.

2. **Spotify API Rate Limits**:
   - Exporting very large playlists may pause temporarily due to Spotify's API rate limits.

---

## Adding Exportify to PATH (Optional)

You can add Exportify to your system PATH to run it from anywhere:

1. Locate the Exportify directory.
2. Add it to your system PATH:
   - On Windows:
     - Go to **System Properties > Advanced System Settings > Environment Variables**.
     - Add the Exportify folder to the PATH variable.
   - On macOS/Linux:
     - Add the following to your shell configuration file (e.g., `.bashrc`, `.zshrc`):
       ```bash
       export PATH="$PATH:/path/to/exportify"
       ```

3. Verify by running:
   ```bash
   python Exportify.py <Spotify Playlist URL>
   ```

---

## Development

### Prerequisites

- Python 3.9+
- Install dependencies:
  ```bash
  pip install spotipy
  ```

### Running the Script

1. Clone the repository:
   ```bash
   git clone https://github.com/your-repo/exportify.git
   cd exportify
   ```

2. Run the script:
   ```bash
   python Exportify.py <Spotify Playlist URL>
   ```

---

## License

This project is licensed under the MIT License. See the `LICENSE` file for details.

---

## Acknowledgments

- [Spotify Developer API](https://developer.spotify.com/documentation/web-api/)
- [Spotipy Library](https://spotipy.readthedocs.io/en/2.16.1/)

---

**Enjoy Exporting Your Playlists with Exportify!**
