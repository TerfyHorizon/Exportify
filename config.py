# config.py
import tomllib
import os

def load_config():
    """Load configuration from config.toml."""
    config_path = os.path.join(os.path.dirname(__file__), "config.toml")
    with open(config_path, "rb") as f:
        return tomllib.load(f)
