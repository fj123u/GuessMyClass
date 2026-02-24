"""
Module de détection de connexion Supabase
Vérifie si la base de données est accessible
"""

from supabase import create_client
import time
import httpx

SUPABASE_URL = "https://dfrfhlvbckvakgtridzv.supabase.co"
SUPABASE_KEY = "sb_publishable_OEqgvVyKwJGXy5rV1H1Y8Q_kGL98num"

# État global de la connexion
_connection_status = None
_last_check_time = 0
_check_interval = 30  # Revérifie toutes les 30 secondes

def check_supabase_connection(force=False):
    """
    Vérifie si Supabase est accessible avec timeout de 3 secondes.
    
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
        # ✅ Timeout de 3 secondes pour ne pas bloquer
        http_client = httpx.Client(timeout=3.0)
        supabase = create_client(
            SUPABASE_URL, 
            SUPABASE_KEY,
            options={"http_client": http_client}
        )
        
        # Test simple : récupère 1 entrée de la table leaderboard
        result = supabase.table("leaderboard")\
            .select("pseudo")\
            .limit(1)\
            .execute()
        
        _connection_status = True
        _last_check_time = current_time
        print("✅ Connexion Supabase : OK")
        return True
        
    except Exception as e:
        _connection_status = False
        _last_check_time = current_time
        print(f"❌ Connexion Supabase : ÉCHEC ({type(e).__name__})")
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