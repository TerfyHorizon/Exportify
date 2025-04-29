# Exportify

**Exportify** is a fully local, cross-platform Python tool that exports Spotify playlists to TXT, CSV, Markdown, or JSON — through a clean Web-based dashboard or command-line interface.


- 🎧 No installation
- 🔒 Fully offline (except Spotify API access)
- 💾 Runs from USB or any folder
- 💻 Works on Linux, macOS, Windows, and Android (via Termux)

---

## ✨ Features

- **Web-Based Interface:** Local Flask WebGUI — dark-themed, mobile-safe, runs at `http://127.0.0.1:5050`
- **CLI Mode with Flags:** Power users can use `--cli`, `--format`, and `--batch`
- **Multiple Export Formats:** 
  - Markdown (`.md`)
  - Plain Text (`.txt`)
  - CSV (`.csv`)
  - JSON (`.json`)
- **Batch Mode:** Export multiple playlists at once from a text file
- **Progress Bar:** Beautiful `tqdm` CLI progress bar during batch exports
- **Fully Offline & Self-Contained:** All data stays on your machine

---

## 🔧 Getting Started

### Prerequisites

1. **Spotify API Credentials**
   - Go to the [Spotify Developer Dashboard](https://developer.spotify.com/dashboard/applications)
   - Create an app and copy your **Client ID** and **Client Secret**

2. **Python 3.13.3 (recommended)**  
   Exportify is developed and tested on Python 3.13.3.  
   Python 3.10+ is likely fine, but the latest version is recommended.

---

### Installation

1. **Clone the project**
   ```bash
   git clone https://github.com/your-username/exportify.git
   cd exportify
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Edit `config.toml`**
   ```toml
   [spotify]
   client_id = "YOUR_CLIENT_ID_HERE"
   client_secret = "YOUR_CLIENT_SECRET_HERE"

   [output]
   output_dir = "playlists"

   [webgui]
   port = 5050
   ```

---

## 🚀 Usage

### 🔹 Web GUI (Default Mode)

```bash
python3 -m exportify
```

- Automatically opens `http://127.0.0.1:5050`
- Paste a Spotify playlist URL
- Select export format
- Click Export

> ✅ All exports saved to the `playlists/` folder

---

### 🔸 CLI Mode

```bash
python3 -m exportify --cli --playlist-url "https://open.spotify.com/playlist/..." --format csv
```

---

### 🔹 Batch Export (CLI)

```bash
python3 -m exportify --cli --batch path/to/file.txt --format json
```

Where `file.txt` contains one playlist URL per line.

Example progress output:
```
Exporting playlists:  75%|███████████████████████████▌     | 3/4 [00:08<00:02, 2.31s/playlist]
```

---

## 📦 Output Example (JSON)

```json
[
  {
    "track_name": "Ride",
    "artist_names": ["Twenty One Pilots"],
    "album_name": "Blurryface"
  }
]
```

---

## 📂 Project Structure

```plaintext
exportify/
├── __main__.py
├── cli.py
├── config.py
├── exportify.py
├── webgui.py
├── templates/
│   ├── base.html
│   ├── index.html
│   └── result.html
├── playlists/
requirements.txt
config.toml
```

---

## ⚠ Known Issues

- Playlist URLs must be valid and public/private Spotify playlists
- Rate-limiting may occur for very large batch exports (Spotify API limitation)
- GUI currently supports single playlist export (batch upload planned for v3.3+)

---

## 🙌 Contributing

PRs welcome!  
Fork and submit your improvements.

---

## 🛠 Built With

- [Spotify Web API](https://developer.spotify.com/documentation/web-api/)
- [Spotipy](https://spotipy.readthedocs.io/)
- [Flask](https://flask.palletsprojects.com/)
- [tqdm](https://tqdm.github.io/) — for CLI progress bars

---

**Export your playlists your way.**  
🎶 Markdown. JSON. Plain Text. CSV.  
💻 Web or CLI. Your data, your control.
