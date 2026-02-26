import sys, os
import pygame
import time
from shape_creator import *
from utils import *
from multiplayer import (get_final_scores, finish_game_session, save_player_game_stats,
                         is_player_guest, get_all_round_results, get_room_info,
                         restart_game_new_code, SOLUTION_COLOR)
from config_manager import get_pseudo
from sql_link import send_score

def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

_stats_saved = {}
_last_poll = {}

replay_button_cached = Shape('replay', 'Rejouer', 200, 70, (current_w/2 - 220, current_h - 100), 3, (0, 200, 0), True, (resource_path("GuessMyClass/font/MightySouly.ttf"), 35))
menu_button_host_cached = Shape('home', 'Menu', 200, 70, (current_w/2 + 20, current_h - 100), 3, (104, 180, 229), True, (resource_path("GuessMyClass/font/MightySouly.ttf"), 35))
menu_button_guest_cached = Shape('home', 'Retour au menu', 300, 70, (current_w/2 - 150, current_h - 100), 3, (104, 180, 229), True, (resource_path("GuessMyClass/font/MightySouly.ttf"), 35))

def final_results_multi_display(room_code, session_id=None, game_start_time=None):
    global _stats_saved, _last_poll
    
    # ✅ Lance la musique de menu
    try:
        from audio_manager import audio
        audio.play_music_menu()
    except:
        pass
    
    if room_code not in _last_poll:
        _last_poll[room_code] = time.time()
    
    if session_id and game_start_time and session_id not in _stats_saved:
        print(f"Sauvegarde stats session {session_id}")
        
        scores = get_final_scores(room_code)
        duration = int(time.time() - game_start_time)
        
        room_info = get_room_info(room_code)
        nb_rounds = room_info["mode"] if room_info else 5
        
        winner = None
        for pseudo, score in scores:
            if not is_player_guest(pseudo):
                winner = pseudo
                break
        
        finish_game_session(session_id, winner, duration)
        all_rounds = get_all_round_results(room_code)
        
        for rank, (pseudo, total_score) in enumerate(scores, 1):
            is_guest = is_player_guest(pseudo)
            if is_guest:
                print(f"Invité ignoré pour stats: {pseudo}")
                continue
            
            rounds_data = [r for r in all_rounds if r['pseudo'] == pseudo]
            if not rounds_data:
                continue
            
            round_scores = [r['score'] for r in rounds_data]
            stats = {
                "total_score": total_score,
                "rank": rank,
                "rounds_played": len(round_scores),
                "avg_score": round(sum(round_scores) / len(round_scores)) if round_scores else 0,
                "best_score": max(round_scores) if round_scores else 0,
                "worst_score": min(round_scores) if round_scores else 0,
                "perfect_guesses": sum(1 for s in round_scores if s >= 4900)
            }
            
            save_player_game_stats(session_id, pseudo, is_guest, stats)
            send_score(pseudo, nb_rounds, total_score)
            print(f"Score envoyé au leaderboard pour {pseudo}: {total_score} pts ({nb_rounds} manches)")
        
        _stats_saved[session_id] = True
    
    room_data = get_room_info(room_code)
    if not room_data:
        if session_id in _stats_saved:
            del _stats_saved[session_id]
        if room_code in _last_poll:
            del _last_poll[room_code]
        leave_button.show()
        return "multiplayer_menu"
    
    pseudo = get_pseudo()  # ✅ Charge depuis JSON
    is_host = room_data["host"] == pseudo
    
    # ✅ Récupère les couleurs des joueurs
    player_colors = room_data.get("player_colors", {})
    
    leave_button.draw()
    
    title = Shape(None, "Résultats finaux", 500, 80, (current_w/2 - 250, 50), 0, (104, 180, 229), False, (resource_path("GuessMyClass/font/MightySouly.ttf"), 60))
    title.draw()
    
    scores = get_final_scores(room_code)
    
    font_score = pygame.font.Font(resource_path("GuessMyClass/font/MightySouly.ttf"), 35)
    
    y = 180
    for i, (pseudo_player, score) in enumerate(scores):
        player_is_guest = is_player_guest(pseudo_player)
        guest_marker = " 👤" if player_is_guest else ""
        
        # ✅ Couleur du joueur
        player_color = tuple(player_colors.get(pseudo_player, [184, 180, 229]))
        
        # Médailles pour les 3 premiers
        if i == 0:
            medal = "🏆"
            text_color = (255, 215, 0)  # Or
        elif i == 1:
            medal = "🥈"
            text_color = (192, 192, 192)  # Argent
        elif i == 2:
            medal = "🥉"
            text_color = (205, 127, 50)  # Bronze
        else:
            medal = f"{i+1}."
            text_color = (200, 200, 200)
        
        # ✅ Carré de couleur du joueur à gauche
        pygame.draw.rect(screen, player_color, (current_w//2 - 280, y + 10, 22, 22), border_radius=4)
        pygame.draw.rect(screen, (0, 0, 0), (current_w//2 - 280, y + 10, 22, 22), 1, border_radius=4)
        
        # Texte du score toujours en noir pour lisibilité
        text = f"{medal} {pseudo_player}{guest_marker}: {score} pts"
        score_text = font_score.render(text, True, (0, 0, 0))
        screen.blit(score_text, (current_w//2 - 250, y))
        
        y += 60
    
    # ✅ Légende des couleurs en bas à gauche
    font_legend = pygame.font.Font(resource_path("GuessMyClass/font/MightySouly.ttf"), 18)
    legend_x = 20
    legend_y = current_h - 160
    
    legend_title = font_legend.render("Couleurs :", True, (0, 0, 0))
    screen.blit(legend_title, (legend_x, legend_y))
    legend_y += 25
    
    for pseudo_player, _ in scores:
        player_color = tuple(player_colors.get(pseudo_player, [184, 180, 229]))
        pygame.draw.rect(screen, player_color, (legend_x, legend_y, 14, 14), border_radius=2)
        pygame.draw.rect(screen, (0, 0, 0), (legend_x, legend_y, 14, 14), 1, border_radius=2)
        name_text = font_legend.render(pseudo_player[:10], True, (0, 0, 0))
        screen.blit(name_text, (legend_x + 20, legend_y - 2))
        legend_y += 20
    
    # ✅ Polling pour non-hôtes
    if not is_host:
        if time.time() - _last_poll[room_code] > 2.0:
            _last_poll[room_code] = time.time()
            try:
                from supabase import create_client
                SUPABASE_URL = "https://dfrfhlvbckvakgtridzv.supabase.co"
                SUPABASE_KEY = "sb_publishable_OEqgvVyKwJGXy5rV1H1Y8Q_kGL98num"
                supabase = create_client(SUPABASE_URL, SUPABASE_KEY)
                
                host_name = room_data["host"]
                result = supabase.table("game_rooms")\
                    .select("*")\
                    .eq("host", host_name)\
                    .eq("status", "waiting")\
                    .order("created_at", desc=True)\
                    .limit(1)\
                    .execute()
                
                if result.data and len(result.data) > 0:
                    new_room = result.data[0]
                    new_room_code = new_room["room_code"]
                    if new_room_code != room_code and pseudo in new_room["players"]:
                        print(f"🎮 Nouvelle partie détectée: {new_room_code}")
                        if session_id in _stats_saved:
                            del _stats_saved[session_id]
                        if room_code in _last_poll:
                            del _last_poll[room_code]
                        return ('waiting_room', new_room_code, False)
            except Exception as e:
                print(f"Erreur polling nouvelle room: {e}")
    
    # Boutons
    if is_host:
        dest = replay_button_cached.draw()
        if dest == 'replay':
            new_room_code = restart_game_new_code(room_code)
            if new_room_code:
                if session_id in _stats_saved:
                    del _stats_saved[session_id]
                if room_code in _last_poll:
                    del _last_poll[room_code]
                return ('waiting_room', new_room_code, True)
        
        dest = menu_button_host_cached.draw()
        if dest == 'home':
            if session_id in _stats_saved:
                del _stats_saved[session_id]
            if room_code in _last_poll:
                del _last_poll[room_code]
            leave_button.show()
            return 'home'
    else:
        dest = menu_button_guest_cached.draw()
        if dest == 'home':
            if session_id in _stats_saved:
                del _stats_saved[session_id]
            if room_code in _last_poll:
                del _last_poll[room_code]
            leave_button.show()
            return 'home'
    
    return None