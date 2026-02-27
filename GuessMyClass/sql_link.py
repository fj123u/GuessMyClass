#Importe les bibliothèques nécessaires pour le fonctionnement du code
import sys, os
from utils import *
from supabase_wrapper import get_supabase, with_timeout

# Obtient le client Supabase via le wrapper
supabase = get_supabase()


@with_timeout(2)
def _send_score_impl(pseudo: str, mode: int, score: int):
    """Implémentation réelle de send_score avec timeout"""
    supabase.table("leaderboard").insert({
        "pseudo": pseudo,
        "mode": mode,
        "score": score
    }).execute()


# Fonction qui envoie un score sur la BDD
def send_score(pseudo: str, mode: int, score: int):
    if not supabase:
        print("❌ Pas de connexion BDD - score non envoyé")
        return False
    
    try:
        _send_score_impl(pseudo, mode, score)
        print(f"✅ Score envoyé: {pseudo} → {score}")
        return True
    except TimeoutError:
        print(f"❌ Timeout envoi score (BDD trop lente)")
        return False
    except Exception as e:
        print(f"❌ Erreur envoi score: {type(e).__name__}")
        return False


@with_timeout(2)
def _get_best_score_impl(pseudo: str, mode: int):
    """Implémentation réelle de get_best_score avec timeout"""
    res = supabase.table("leaderboard") \
        .select("score") \
        .eq("pseudo", pseudo) \
        .eq("mode", mode) \
        .order("score", desc=True) \
        .limit(1) \
        .execute()
    
    if res.data:
        return res.data[0]["score"]
    return 0


# Fonction pour récupérer le meilleur score du joueur
def get_best_score(pseudo: str, mode: int):
    if not supabase:
        print("❌ Pas de connexion BDD - score = 0")
        return 0
    
    try:
        return _get_best_score_impl(pseudo, mode)
    except TimeoutError:
        print(f"❌ Timeout récupération best score (BDD trop lente)")
        return 0
    except Exception as e:
        print(f"❌ Erreur récupération best score: {type(e).__name__}")
        return 0


@with_timeout(2)
def _get_leaderboard_impl(mode: int):
    """Implémentation réelle de get_leaderboard avec timeout"""
    res = supabase.table("leaderboard") \
        .select("pseudo, score") \
        .eq("mode", mode) \
        .order("score", desc=True) \
        .execute()
    
    best_scores = {}
    for row in res.data:
        pseudo = row['pseudo']
        score = row['score']
        if pseudo not in best_scores or score > best_scores[pseudo]:
            best_scores[pseudo] = score
    
    leaderboard = [{'pseudo': pseudo, 'score': score} 
                   for pseudo, score in best_scores.items()]
    leaderboard.sort(key=lambda x: x['score'], reverse=True)
    
    return leaderboard


# Fonction pour récupérer l'ensemble des données de la BDD
def get_leaderboard(mode: int, limit: int = 20):
    if not supabase:
        print("❌ Pas de connexion BDD - leaderboard vide")
        return []
    
    try:
        leaderboard = _get_leaderboard_impl(mode)
        return leaderboard[:limit]
    except TimeoutError:
        print(f"❌ Timeout récupération leaderboard (BDD trop lente)")
        return []
    except Exception as e:
        print(f"❌ Erreur récupération leaderboard: {type(e).__name__}")
        return []


# Fonction qui créer un fichier local pour save le best_score de l'utilisateur
def save_local_profile(pseudo):
    try:
        path = resource_path("GuessMyClass/profile/compte.txt")
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "w", encoding="utf-8") as f:
            f.write(pseudo)
        return True
    except Exception as e:
        print(f"❌ Erreur sauvegarde profil local: {e}")
        return False


# Fonction qui récupère le score sur la save locale
def load_local_profile():
    try:
        with open(resource_path("GuessMyClass/profile/compte.txt"), "r", encoding="utf-8") as f:
            return f.read().strip()
    except FileNotFoundError:
        return ""
    except Exception as e:
        print(f"❌ Erreur lecture profil local: {e}")
        return ""