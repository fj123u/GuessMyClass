"""
Gestionnaire de configuration du jeu
Sauvegarde : pseudo, volumes, résolution
Compatible .py et .exe (PyInstaller)
"""

import json
import os
from pathlib import Path
import platform


# ==========================================================
# 📁 Définition du dossier de sauvegarde utilisateur
# ==========================================================

if platform.system() == "Windows":
    BASE_DIR = Path(os.getenv("APPDATA"))
else:
    BASE_DIR = Path.home() / ".config"

APPDATA_DIR = BASE_DIR / "GuessMyClass"
CONFIG_FILE = APPDATA_DIR / "settings.json"


# ==========================================================
# ⚙️ Configuration par défaut
# ==========================================================

DEFAULT_CONFIG = {
    "pseudo": "Invite",
    "music_volume": 0.3,
    "sfx_volume": 0.5,
    "resolution": {
        "width": 1920,
        "height": 1080,
        "fullscreen": False
    }
}

# Cache global pour éviter lectures multiples
_config_cache = None


# ==========================================================
# 📥 Chargement
# ==========================================================

def load_config():
    """Charge la configuration depuis le fichier JSON (avec cache)"""
    global _config_cache

    if _config_cache is not None:
        return _config_cache.copy()

    try:
        if CONFIG_FILE.exists():
            with open(CONFIG_FILE, "r", encoding="utf-8") as f:
                config = json.load(f)
                _config_cache = config
                return config.copy()
        else:
            save_config(DEFAULT_CONFIG)
            return DEFAULT_CONFIG.copy()

    except Exception as e:
        print(f"❌ Erreur lecture config: {e}")
        return DEFAULT_CONFIG.copy()


# ==========================================================
# 💾 Sauvegarde
# ==========================================================

def save_config(config):
    """Sauvegarde la configuration dans le fichier JSON"""
    global _config_cache

    try:
        APPDATA_DIR.mkdir(parents=True, exist_ok=True)

        with open(CONFIG_FILE, "w", encoding="utf-8") as f:
            json.dump(config, f, indent=4, ensure_ascii=False)

        _config_cache = config.copy()
        return True

    except Exception as e:
        print(f"❌ Erreur sauvegarde config: {e}")
        return False


# ==========================================================
# 🎮 Accesseurs pratiques
# ==========================================================

def get_pseudo():
    config = load_config()
    return config.get("pseudo", "Invite")


def set_pseudo(pseudo):
    config = load_config()
    config["pseudo"] = pseudo
    save_config(config)


def get_volumes():
    config = load_config()
    return config.get("music_volume", 0.3), config.get("sfx_volume", 0.5)


def set_volumes(music_vol, sfx_vol):
    config = load_config()
    config["music_volume"] = music_vol
    config["sfx_volume"] = sfx_vol
    save_config(config)


def get_resolution():
    config = load_config()
    res = config.get("resolution", DEFAULT_CONFIG["resolution"])
    return res["width"], res["height"], res.get("fullscreen", False)


def set_resolution(width, height, fullscreen=False):
    config = load_config()
    config["resolution"] = {
        "width": width,
        "height": height,
        "fullscreen": fullscreen
    }
    save_config(config)