import sys, os
import pygame
import time
from shape_creator import *
from utils import *
from multiplayer import get_final_scores, finish_game_session, save_player_game_stats, is_player_guest, get_all_round_results, get_room_info, restart_game_new_code
from sql_link import load_local_profile, send_score

def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

_stats_saved = {}

# Boutons UNE SEULE FOIS
replay_button_cached = Shape('replay', 'Rejouer', 200, 70, (current_w/2 - 220, current_h - 100), 3, (0, 200, 0), True, (resource_path("GuessMyClass/font/MightySouly.ttf"), 35))
menu_button_host_cached = Shape('home', 'Menu', 200, 70, (current_w/2 + 20, current_h - 100), 3, (104, 180, 229), True, (resource_path("GuessMyClass/font/MightySouly.ttf"), 35))
menu_button_guest_cached = Shape('home', 'Retour au menu', 300, 70, (current_w/2 - 150, current_h - 100), 3, (104, 180, 229), True, (resource_path("GuessMyClass/font/MightySouly.ttf"), 35))

def final_results_multi_display(room_code, session_id=None, game_start_time=None):
    global _stats_saved
    
    # Sauvegarde UNE FOIS
    if session_id and game_start_time and session_id not in _stats_saved:
        print(f"Sauvegarde stats session {session_id}")
        
        scores = get_final_scores(room_code)
        duration = int(time.time() - game_start_time)
        
        # Récupère les infos de la room pour savoir le mode (nb de manches)
        room_info = get_room_info(room_code)
        nb_rounds = room_info["mode"] if room_info else 5
        
        # Trouve le gagnant (exclu les invités)
        winner = None
        for pseudo, score in scores:
            if not is_player_guest(pseudo):
                winner = pseudo
                break
        
        finish_game_session(session_id, winner, duration)
        
        all_rounds = get_all_round_results(room_code)
        
        # Sauvegarde SEULEMENT les vrais joueurs
        for rank, (pseudo, total_score) in enumerate(scores, 1):
            is_guest = is_player_guest(pseudo)
            
            if is_guest:
                print(f"Invité ignoré: {pseudo}")
                continue
            
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
                
                save_player_game_stats(session_id, pseudo, is_guest, stats)
                
                # Envoie aussi au LEADERBOARD
                send_score(pseudo, nb_rounds, total_score)
                print(f"Score envoyé au leaderboard pour {pseudo}: {total_score} pts ({nb_rounds} manches)")
        
        _stats_saved[session_id] = True
    
    room_data = get_room_info(room_code)
    if not room_data:
        if session_id in _stats_saved:
            del _stats_saved[session_id]
        # IMPORTANT: Réaffiche le bouton leave avant de quitter
        leave_button.show()
        return "multiplayer_menu"
    
    pseudo = load_local_profile()
    is_host = room_data["host"] == pseudo
    
    leave_button.draw()
    
    title = Shape(None, "Résultats finaux", 500, 80, (current_w/2 - 250, 50), 0, (104, 180, 229), False, (resource_path("GuessMyClass/font/MightySouly.ttf"), 60))
    title.draw()
    
    scores = get_final_scores(room_code)
    
    y = 180
    for i, (pseudo_player, score) in enumerate(scores):
        # Marque les invités
        player_is_guest = is_player_guest(pseudo_player)
        guest_marker = " 👤" if player_is_guest else ""
        
        if i == 0:
            text = f"🏆 {pseudo_player}{guest_marker}: {score} pts"
            color = (255, 215, 0)
        elif i == 1:
            text = f"🥈 {pseudo_player}{guest_marker}: {score} pts"
            color = (192, 192, 192)
        elif i == 2:
            text = f"🥉 {pseudo_player}{guest_marker}: {score} pts"
            color = (205, 127, 50)
        else:
            text = f"{i+1}. {pseudo_player}{guest_marker}: {score} pts"
            color = (184, 180, 229)
        
        score_shape = Shape(None, text, 500, 50, (current_w/2 - 250, y), 0, color, False, (resource_path("GuessMyClass/font/MightySouly.ttf"), 35))
        score_shape.draw()
        y += 60
    
    if is_host:
        dest = replay_button_cached.draw()
        if dest == 'replay':
            new_room_code = restart_game_new_code(room_code)
            if new_room_code:
                if session_id in _stats_saved:
                    del _stats_saved[session_id]
                return ('waiting_room', new_room_code, True)
        
        dest = menu_button_host_cached.draw()
        if dest == 'home':
            if session_id in _stats_saved:
                del _stats_saved[session_id]
            # IMPORTANT: Réaffiche le bouton leave
            leave_button.show()
            return 'home'
    else:
        dest = menu_button_guest_cached.draw()
        if dest == 'home':
            if session_id in _stats_saved:
                del _stats_saved[session_id]
            # IMPORTANT: Réaffiche le bouton leave
            leave_button.show()
            return 'home'
    
    return None