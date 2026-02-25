"""
Module de détection de connexion Supabase
Vérifie si la base de données est accessible
"""

from supabase import create_client
import time
import httpx
from httpx import Timeout

SUPABASE_URL = "https://dfrfhlvbckvakgtridzv.supabase.co"
SUPABASE_KEY = "sb_publishable_OEqgvVyKwJGXy5rV1H1Y8Q_kGL98num"

# État global de la connexion
_connection_status = None
_last_check_time = 0
_check_interval = 30  # Revérifie toutes les 30 secondes

def check_supabase_connection(force=False):
    """
    Vérifie si Supabase est accessible avec timeout de 2 secondes.
    
    Args:
        force (bool): Force une nouvelle vérification même si cache valide
    
    Returns:
        bool: True si connecté, False sinon
    """
    global _connection_status, _last_check_time
    
    current_time = time.time()
    
    # Utilise le cache si récent (sauf si force=True)
    if not force and _connection_status is not None and (current_time - _last_check_time) < _check_interval:
        return _connection_status
    
    try:
        # ✅ Test HTTP simple avec timeout court (2s)
        timeout = Timeout(2.0, connect=2.0)
        client = httpx.Client(timeout=timeout)
        
        # Test direct de l'API REST Supabase
        url = f"{SUPABASE_URL}/rest/v1/leaderboard?limit=1"
        headers = {
            "apikey": SUPABASE_KEY,
            "Authorization": f"Bearer {SUPABASE_KEY}"
        }
        
        response = client.get(url, headers=headers)
        client.close()
        
        if response.status_code == 200:
            _connection_status = True
            _last_check_time = current_time
            print("✅ Connexion Supabase : OK")
            return True
        else:
            _connection_status = False
            _last_check_time = current_time
            print(f"❌ Connexion Supabase : ÉCHEC (HTTP {response.status_code})")
            return False
        
    except (httpx.TimeoutException, httpx.ConnectTimeout, httpx.ReadTimeout) as e:
        _connection_status = False
        _last_check_time = current_time
        print(f"❌ Connexion Supabase : TIMEOUT (pas de réponse en 2s)")
        return False
        
    except Exception as e:
        _connection_status = False
        _last_check_time = current_time
        print(f"❌ Connexion Supabase : ÉCHEC ({type(e).__name__}: {str(e)})")
        return False

def is_online():
    """Retourne l'état de connexion actuel (utilise le cache)"""
    if _connection_status is None:
        return check_supabase_connection()
    return _connection_status

def reset_connection_status():
    """Force une nouvelle vérification à la prochaine demande"""
    global _connection_status, _last_check_time
    _connection_status = None
    _last_check_time = 0