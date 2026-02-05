import sys, os
import pygame
import time
from shape_creator import *
from utils import *
from multiplayer import get_final_scores, finish_game_session, save_player_game_stats, is_player_guest, get_all_round_results

def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

# Variable globale pour éviter de sauvegarder plusieurs fois
_stats_saved = {}

def final_results_multi_display(room_code, session_id=None, game_start_time=None):
    global _stats_saved
    
    leave_button.draw()
    
    title = Shape(None, "Résultats finaux", 500, 80, (current_w/2 - 250, 50), 0, (104, 180, 229), False, (resource_path("GuessMyClass/font/MightySouly.ttf"), 60))
    title.draw()
    
    scores = get_final_scores(room_code)
    
    # Sauvegarde UNE SEULE FOIS en utilisant session_id comme clé
    if session_id and game_start_time and session_id not in _stats_saved:
        print(f"Sauvegarde des stats pour session {session_id}")
        duration = int(time.time() - game_start_time)
        winner = scores[0][0] if scores else None
        
        finish_game_session(session_id, winner, duration)
        
        # Récupère TOUS les rounds pour calculer les stats
        all_rounds = get_all_round_results(room_code)
        
        # Sauvegarde les stats de chaque joueur
        for rank, (pseudo, total_score) in enumerate(scores, 1):
            # Filtre les rounds du joueur
            player_rounds = [r for r in all_rounds if r['pseudo'] == pseudo]
            
            if player_rounds:
                round_scores = [r['score'] for r in player_rounds]
                
                stats = {
                    "total_score": total_score,
                    "rank": rank,
                    "rounds_played": len(player_rounds),
                    "avg_score": int(total_score / len(player_rounds)),
                    "best_score": max(round_scores),
                    "worst_score": min(round_scores),
                    "perfect_guesses": sum(1 for s in round_scores if s >= 4900)
                }
                
                is_guest = is_player_guest(pseudo)
                save_player_game_stats(session_id, pseudo, is_guest, stats)
                print(f"Stats sauvegardées pour {pseudo}: {stats}")
        
        # Marque cette session comme sauvegardée
        _stats_saved[session_id] = True
    
    y = 180
    for i, (pseudo, score) in enumerate(scores):
        if i == 0:
            text = f"🏆 {pseudo}: {score} pts"
            color = (255, 215, 0)
        elif i == 1:
            text = f"🥈 {pseudo}: {score} pts"
            color = (192, 192, 192)
        elif i == 2:
            text = f"🥉 {pseudo}: {score} pts"
            color = (205, 127, 50)
        else:
            text = f"{i+1}. {pseudo}: {score} pts"
            color = (184, 180, 229)
        
        score_shape = Shape(None, text, 500, 50, (current_w/2 - 250, y), 0, color, False, (resource_path("GuessMyClass/font/MightySouly.ttf"), 35))
        score_shape.draw()
        y += 60
    
    home_button = Shape('home', 'Retour au menu', 300, 70, (current_w/2 - 150, current_h - 100), 3, (104, 180, 229), True, (resource_path("GuessMyClass/font/MightySouly.ttf"), 35))
    dest = home_button.draw()
    if dest:
        # Réinitialise le cache quand on quitte
        if session_id in _stats_saved:
            del _stats_saved[session_id]
        return dest
    
    return ('final_results_multi', room_code)