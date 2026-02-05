import sys, os
import pygame
import time
from shape_creator import *
from utils import *
from multiplayer import get_final_scores, finish_game_session, save_player_game_stats, is_player_guest, get_all_round_results, get_room_info, restart_game
from sql_link import load_local_profile

def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

# Variables globales
_stats_saved = {}
_last_check_time = 0

# Boutons créés UNE SEULE FOIS en dehors de la fonction
replay_button_cached = Shape('replay', 'Rejouer', 200, 70, (current_w/2 - 220, current_h - 100), 3, (0, 200, 0), True, (resource_path("GuessMyClass/font/MightySouly.ttf"), 35))
menu_button_host_cached = Shape('home', 'Menu', 200, 70, (current_w/2 + 20, current_h - 100), 3, (104, 180, 229), True, (resource_path("GuessMyClass/font/MightySouly.ttf"), 35))
menu_button_guest_cached = Shape('home', 'Retour au menu', 300, 70, (current_w/2 - 150, current_h - 100), 3, (104, 180, 229), True, (resource_path("GuessMyClass/font/MightySouly.ttf"), 35))

def final_results_multi_display(room_code, session_id=None, game_start_time=None):
    global _stats_saved, _last_check_time
    
    # Sauvegarde UNE SEULE FOIS
    if session_id and game_start_time and session_id not in _stats_saved:
        print(f"Sauvegarde des stats pour session {session_id}")
        
        scores = get_final_scores(room_code)
        duration = int(time.time() - game_start_time)
        winner = scores[0][0] if scores else None
        
        finish_game_session(session_id, winner, duration)
        
        all_rounds = get_all_round_results(room_code)
        
        for rank, (pseudo, total_score) in enumerate(scores, 1):
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
                print(f"Stats sauvegardées pour {pseudo}")
        
        _stats_saved[session_id] = True
    
    # Récupère les infos de la room
    room_data = get_room_info(room_code)
    if not room_data:
        if session_id in _stats_saved:
            del _stats_saved[session_id]
        return "multiplayer_menu"
    
    pseudo = load_local_profile()
    is_host = room_data["host"] == pseudo
    
    # Vérifie si l'hôte a demandé à rejouer (toutes les secondes)
    current_time = time.time()
    if not is_host and current_time - _last_check_time > 1.0:
        room_data = get_room_info(room_code)
        if room_data and room_data["status"] == "waiting":
            # L'hôte a relancé la partie !
            _last_check_time = current_time
            if session_id in _stats_saved:
                del _stats_saved[session_id]
            return ('waiting_room', room_code, False)
        _last_check_time = current_time
    
    # Affichage
    leave_button.draw()
    
    title = Shape(None, "Résultats finaux", 500, 80, (current_w/2 - 250, 50), 0, (104, 180, 229), False, (resource_path("GuessMyClass/font/MightySouly.ttf"), 60))
    title.draw()
    
    scores = get_final_scores(room_code)
    
    y = 180
    for i, (pseudo_player, score) in enumerate(scores):
        if i == 0:
            text = f"🏆 {pseudo_player}: {score} pts"
            color = (255, 215, 0)
        elif i == 1:
            text = f"🥈 {pseudo_player}: {score} pts"
            color = (192, 192, 192)
        elif i == 2:
            text = f"🥉 {pseudo_player}: {score} pts"
            color = (205, 127, 50)
        else:
            text = f"{i+1}. {pseudo_player}: {score} pts"
            color = (184, 180, 229)
        
        score_shape = Shape(None, text, 500, 50, (current_w/2 - 250, y), 0, color, False, (resource_path("GuessMyClass/font/MightySouly.ttf"), 35))
        score_shape.draw()
        y += 60
    
    # Boutons en bas
    if is_host:
        # Hôte : 2 boutons (Rejouer + Menu)
        dest = replay_button_cached.draw()
        if dest == 'replay':
            print("HÔTE: Rejouer cliqué")
            restart_game(room_code)
            pygame.time.delay(500)
            if session_id in _stats_saved:
                del _stats_saved[session_id]
            return ('waiting_room', room_code, True)
        
        dest = menu_button_host_cached.draw()
        if dest == 'home':
            print("HÔTE: Menu cliqué")
            if session_id in _stats_saved:
                del _stats_saved[session_id]
            return 'home'
    else:
        # Invité : Juste le bouton Menu
        dest = menu_button_guest_cached.draw()
        if dest == 'home':
            print("INVITÉ: Menu cliqué")
            if session_id in _stats_saved:
                del _stats_saved[session_id]
            return 'home'
    
    # Ne retourne RIEN si aucun bouton n'est cliqué (évite la boucle)
    return None