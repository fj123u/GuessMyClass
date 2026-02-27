"""
Wrapper Supabase avec timeout automatique sur toutes les requêtes
"""

from supabase import create_client
import threading
from functools import wraps

SUPABASE_URL = "https://dfrfhlvbckvakgtridzv.supabase.co"
SUPABASE_KEY = "sb_publishable_OEqgvVyKwJGXy5rV1H1Y8Q_kGL98num"

# Client Supabase global
_supabase_client = None

def get_supabase():
    """Retourne le client Supabase (singleton)"""
    global _supabase_client
    if _supabase_client is None:
        try:
            _supabase_client = create_client(SUPABASE_URL, SUPABASE_KEY)
            print("✅ Supabase wrapper initialisé")
        except Exception as e:
            print(f"❌ Erreur init Supabase wrapper: {e}")
            _supabase_client = None
    return _supabase_client


def with_timeout(timeout_seconds=2):
    """
    Décorateur qui ajoute un timeout à une fonction Supabase.
    Si la fonction prend plus de timeout_seconds, elle lève TimeoutError.
    """
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            result = [None]
            exception = [None]
            
            def target():
                try:
                    result[0] = func(*args, **kwargs)
                except Exception as e:
                    exception[0] = e
            
            thread = threading.Thread(target=target, daemon=True)
            thread.start()
            thread.join(timeout=timeout_seconds)
            
            if thread.is_alive():
                print(f"⏱️ Timeout {timeout_seconds}s sur {func.__name__}")
                raise TimeoutError(f"Opération {func.__name__} a dépassé {timeout_seconds}s")
            
            if exception[0]:
                raise exception[0]
            
            return result[0]
        
        return wrapper
    return decorator