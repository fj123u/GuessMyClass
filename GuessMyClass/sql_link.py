#Importe les bibliothèques nécessaires pour le fonctionnement du code
import sys, os
import httpx
from supabase import create_client
from utils import *

SUPABASE_URL = "https://dfrfhlvbckvakgtridzv.supabase.co"
SUPABASE_KEY = "sb_publishable_OEqgvVyKwJGXy5rV1H1Y8Q_kGL98num"

# ✅ Initialisation sécurisée avec timeout de 3 secondes
try:
    http_client = httpx.Client(timeout=3.0)
    supabase = create_client(
        SUPABASE_URL, 
        SUPABASE_KEY,
        options={"http_client": http_client}
    )
except Exception as e:
    print(f"❌ Erreur initialisation Supabase: {e}")
    supabase = None


# Fonction qui envoie un score sur la BDD
def send_score(pseudo: str, mode: int, score: int):
    if not supabase:
        print("❌ Pas de connexion BDD - score non envoyé")
        return False
    
    try:
        supabase.table("leaderboard").insert({
            "pseudo": pseudo,
            "mode": mode,
            "score": score
        }).execute()
        print(f"✅ Score envoyé: {pseudo} → {score}")
        return True
    except Exception as e:
        print(f"❌ Erreur envoi score (connexion coupée ?): {e}")
        return False


# Fonction pour récupérer le meilleur score du joueur
def get_best_score(pseudo: str, mode: int):
    if not supabase:
        print("❌ Pas de connexion BDD - score = 0")
        return 0
    
    try:
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
    
    except Exception as e:
        print(f"❌ Erreur récupération best score (connexion coupée ?): {e}")
        return 0


# Fonction pour récupérer l'ensemble des données de la BDD
def get_leaderboard(mode: int, limit: int = 20):
    if not supabase:
        print("❌ Pas de connexion BDD - leaderboard vide")
        return []
    
    try:
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
        
        return leaderboard[:limit]
    
    except Exception as e:
        print(f"❌ Erreur récupération leaderboard (connexion coupée ?): {e}")
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