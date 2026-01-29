
#Importe les bibliothèques nécessaires pour le fonctionnement du code

import sys, os
from supabase import create_client
from utils import *

SUPABASE_URL = "https://dfrfhlvbckvakgtridzv.supabase.co"
SUPABASE_KEY = "sb_publishable_OEqgvVyKwJGXy5rV1H1Y8Q_kGL98num"

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)


# Fonction qui envoie un score sur la BDD
def send_score(pseudo: str, mode: int, score: int):
   
    supabase.table("leaderboard").insert({
        "pseudo": pseudo,
        "mode": mode,
        "score": score
    }).execute()


# Fonction pour récupérer le meilleur score du joueur
def get_best_score(pseudo: str, mode: int):
    
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


# Fonction pour récupérer l'ensemble des données de la BDD
def get_leaderboard(mode: int, limit: int = 20):
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


# Fonction qui créer un fichier local pour save le best_score de l'utilisateur
def save_local_profile(pseudo):
    path = resource_path("GuessMyClass/profile/compte.txt")
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(pseudo)


# Fonction qui récupère le score sur la save locale
def load_local_profile():
    try:
        with open(resource_path("GuessMyClass/profile/compte.txt"), "r", encoding="utf-8") as f:
            return f.read().strip()
    except FileNotFoundError:
        return ""
