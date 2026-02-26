"""
Gestionnaire de configuration du jeu
Sauvegarde : pseudo, volumes, résolution
"""

import json
import os
import sys

def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)


# ✅ Chemin relatif au script (pas resource_path qui cherche dans le .exe)
CONFIG_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "config")
CONFIG_FILE = os.path.join(CONFIG_DIR, "settings.json")

# Configuration par défaut
DEFAULT_CONFIG = {
    "pseudo": "Invité",
    "music_volume": 0.3,
    "sfx_volume": 0.5,
    "resolution": {
        "width": 1920,
        "height": 1080,
        "fullscreen": False
    }
}

# ✅ Cache global pour éviter les lectures multiples
_config_cache = None


def load_config():
    """Charge la configuration depuis le fichier JSON (avec cache)"""
    global _config_cache
    
    # Utilise le cache si disponible
    if _config_cache is not None:
        return _config_cache.copy()
    
    try:
        if os.path.exists(CONFIG_FILE):
            with open(CONFIG_FILE, "r", encoding="utf-8") as f:
                config = json.load(f)
                _config_cache = config
                print(f"✅ Configuration chargée depuis {CONFIG_FILE}")
                return config.copy()
        else:
            print(f"ℹ️ Pas de config trouvée, création avec valeurs par défaut")
            save_config(DEFAULT_CONFIG)
            return DEFAULT_CONFIG.copy()
    except Exception as e:
        print(f"❌ Erreur lecture config: {e}")
        return DEFAULT_CONFIG.copy()


def save_config(config):
    """Sauvegarde la configuration dans le fichier JSON"""
    global _config_cache
    
    try:
        os.makedirs(CONFIG_DIR, exist_ok=True)
        with open(CONFIG_FILE, "w", encoding="utf-8") as f:
            json.dump(config, f, indent=4, ensure_ascii=False)
        
        # ✅ Met à jour le cache
        _config_cache = config.copy()
        
        # ✅ Affiche seulement si ce n'est pas le premier enregistrement
        if _config_cache != DEFAULT_CONFIG:
            print(f"✅ Configuration sauvegardée")
        return True
    except Exception as e:
        print(f"❌ Erreur sauvegarde config: {e}")
        return False


def get_pseudo():
    """Récupère le pseudo"""
    config = load_config()
    return config.get("pseudo", "Invité")


def set_pseudo(pseudo):
    """Sauvegarde le pseudo"""
    config = load_config()
    config["pseudo"] = pseudo
    save_config(config)


def get_volumes():
    """Récupère les volumes (music, sfx)"""
    config = load_config()
    return config.get("music_volume", 0.3), config.get("sfx_volume", 0.5)


def set_volumes(music_vol, sfx_vol):
    """Sauvegarde les volumes"""
    config = load_config()
    config["music_volume"] = music_vol
    config["sfx_volume"] = sfx_vol
    save_config(config)


def get_resolution():
    """Récupère la résolution (width, height, fullscreen)"""
    config = load_config()
    res = config.get("resolution", DEFAULT_CONFIG["resolution"])
    return res["width"], res["height"], res.get("fullscreen", False)


def set_resolution(width, height, fullscreen=False):
    """Sauvegarde la résolution"""
    config = load_config()
    config["resolution"] = {
        "width": width,
        "height": height,
        "fullscreen": fullscreen
    }
    save_config(config)