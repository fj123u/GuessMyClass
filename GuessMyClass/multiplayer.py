import random
import string
from supabase import create_client
import time
from datetime import datetime, timedelta, timezone

SUPABASE_URL = "https://dfrfhlvbckvakgtridzv.supabase.co"
SUPABASE_KEY = "sb_publishable_OEqgvVyKwJGXy5rV1H1Y8Q_kGL98num"
supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

def generate_room_code():
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))

def cleanup_old_rooms():
    """Supprime les parties en attente de plus de 10 minutes"""
    try:
        ten_minutes_ago = (datetime.now(timezone.utc) - timedelta(minutes=10)).isoformat()
        supabase.table("game_rooms")\
            .delete()\
            .eq("status", "waiting")\
            .lt("created_at", ten_minutes_ago)\
            .execute()
    except Exception as e:
        print(f"Erreur cleanup: {e}")

def create_room(pseudo, mode=5):
    room_code = generate_room_code()
    try:
        cleanup_old_rooms()
        supabase.table("game_rooms").insert({
            "room_code": room_code,
            "host": pseudo,
            "players": [pseudo],
            "mode": mode,
            "status": "waiting"
        }).execute()
        return room_code
    except Exception as e:
        print(f"Erreur création room: {e}")
        return None

def join_room(room_code, pseudo):
    try:
        cleanup_old_rooms()
        
        result = supabase.table("game_rooms")\
            .select("*")\
            .eq("room_code", room_code)\
            .eq("status", "waiting")\
            .single()\
            .execute()
        
        if not result.data:
            return None
        
        try:
            created_at_str = result.data["created_at"].replace('Z', '+00:00')
            created_at = datetime.fromisoformat(created_at_str)
            now = datetime.now(timezone.utc)
            
            if now - created_at > timedelta(minutes=10):
                supabase.table("game_rooms").delete().eq("room_code", room_code).execute()
                return None
        except Exception as date_error:
            print(f"Erreur vérification date: {date_error}")
        
        players = result.data["players"]
        if pseudo not in players:
            players.append(pseudo)
            supabase.table("game_rooms")\
                .update({"players": players})\
                .eq("room_code", room_code)\
                .execute()
        
        return result.data
    except Exception as e:
        print(f"Erreur join room: {e}")
        return None

def get_room_info(room_code):
    try:
        result = supabase.table("game_rooms")\
            .select("*")\
            .eq("room_code", room_code)\
            .single()\
            .execute()
        return result.data
    except Exception as e:
        print(f"Erreur get room: {e}")
        return None

def start_game(room_code, first_room):
    try:
        supabase.table("game_rooms")\
            .update({
                "status": "playing",
                "current_round": 1,
                "current_room": first_room
            })\
            .eq("room_code", room_code)\
            .execute()
        return True
    except Exception as e:
        print(f"Erreur start game: {e}")
        return False

def restart_game(room_code):
    """Remet la partie en attente pour rejouer (garde les joueurs)"""
    try:
        # Supprime les anciennes réponses
        supabase.table("game_answers")\
            .delete()\
            .eq("room_code", room_code)\
            .execute()
        
        # Remet la room en status waiting
        supabase.table("game_rooms")\
            .update({
                "status": "waiting",
                "current_round": 0,
                "current_room": None
            })\
            .eq("room_code", room_code)\
            .execute()
        
        return True
    except Exception as e:
        print(f"Erreur restart game: {e}")
        return False

def next_round(room_code, next_room_name):
    try:
        room = get_room_info(room_code)
        new_round = room["current_round"] + 1
        
        supabase.table("game_rooms")\
            .update({
                "current_round": new_round,
                "current_room": next_room_name
            })\
            .eq("room_code", room_code)\
            .execute()
        return True
    except Exception as e:
        print(f"Erreur next round: {e}")
        return False

def finish_game(room_code):
    try:
        supabase.table("game_rooms")\
            .update({"status": "finished"})\
            .eq("room_code", room_code)\
            .execute()
        return True
    except Exception as e:
        print(f"Erreur finish game: {e}")
        return False

def submit_answer(room_code, round_num, pseudo, x, y, etage, score):
    try:
        supabase.table("game_answers").insert({
            "room_code": room_code,
            "round": round_num,
            "pseudo": pseudo,
            "x": x,
            "y": y,
            "etage": etage,
            "score": score
        }).execute()
        return True
    except Exception as e:
        print(f"Erreur submit answer: {e}")
        return False

def get_round_results(room_code, round_num):
    try:
        result = supabase.table("game_answers")\
            .select("*")\
            .eq("room_code", room_code)\
            .eq("round", round_num)\
            .execute()
        return result.data
    except Exception as e:
        print(f"Erreur get results: {e}")
        return []

def get_all_round_results(room_code):
    """Récupère TOUS les résultats pour un room_code"""
    try:
        result = supabase.table("game_answers")\
            .select("*")\
            .eq("room_code", room_code)\
            .order("round")\
            .execute()
        return result.data
    except Exception as e:
        print(f"Erreur get all results: {e}")
        return []

def get_final_scores(room_code):
    try:
        result = supabase.table("game_answers")\
            .select("pseudo, score")\
            .eq("room_code", room_code)\
            .execute()
        
        scores = {}
        for answer in result.data:
            pseudo = answer["pseudo"]
            score = answer["score"]
            if pseudo in scores:
                scores[pseudo] += score
            else:
                scores[pseudo] = score
        
        sorted_scores = sorted(scores.items(), key=lambda x: x[1], reverse=True)
        return sorted_scores
    except Exception as e:
        print(f"Erreur get final scores: {e}")
        return []

def leave_room(room_code, pseudo):
    try:
        room = get_room_info(room_code)
        if not room:
            return False
        
        players = room["players"]
        if pseudo in players:
            players.remove(pseudo)
            
            if len(players) == 0:
                supabase.table("game_rooms")\
                    .delete()\
                    .eq("room_code", room_code)\
                    .execute()
            else:
                update_data = {"players": players}
                if room["host"] == pseudo:
                    update_data["host"] = players[0]
                
                supabase.table("game_rooms")\
                    .update(update_data)\
                    .eq("room_code", room_code)\
                    .execute()
        
        return True
    except Exception as e:
        print(f"Erreur leave room: {e}")
        return False

# ===== FONCTIONS POUR SAUVEGARDER LES STATS =====

def create_game_session(room_code, mode, total_players):
    """Crée une session de jeu dans la BDD"""
    try:
        result = supabase.table("game_sessions").insert({
            "room_code": room_code,
            "mode": mode,
            "game_type": "multiplayer",
            "total_players": total_players
        }).execute()
        return result.data[0]["id"] if result.data else None
    except Exception as e:
        print(f"Erreur création session: {e}")
        return None

def finish_game_session(session_id, winner_pseudo, duration_seconds):
    """Termine une session de jeu"""
    try:
        supabase.table("game_sessions").update({
            "finished_at": datetime.now(timezone.utc).isoformat(),
            "duration_seconds": duration_seconds,
            "winner_pseudo": winner_pseudo
        }).eq("id", session_id).execute()
        return True
    except Exception as e:
        print(f"Erreur fin de session: {e}")
        return False

def save_round_detail(session_id, round_num, room_name, pseudo, x, y, floor, score, distance, time_taken=None):
    """Sauvegarde les détails d'une manche"""
    try:
        supabase.table("round_details").insert({
            "game_session_id": session_id,
            "round_number": round_num,
            "room_name": room_name,
            "pseudo": pseudo,
            "x_position": x,
            "y_position": y,
            "floor": floor,
            "score": score,
            "distance_from_target": distance,
            "time_taken_seconds": time_taken
        }).execute()
        return True
    except Exception as e:
        print(f"Erreur sauvegarde round: {e}")
        return False

def save_player_game_stats(session_id, pseudo, is_guest, stats):
    """Sauvegarde les stats d'un joueur pour une partie"""
    try:
        supabase.table("player_game_stats").insert({
            "game_session_id": session_id,
            "pseudo": pseudo,
            "is_guest": is_guest,
            "total_score": stats.get("total_score", 0),
            "final_rank": stats.get("rank", 0),
            "rounds_played": stats.get("rounds_played", 0),
            "average_score_per_round": stats.get("avg_score", 0),
            "best_round_score": stats.get("best_score", 0),
            "worst_round_score": stats.get("worst_score", 0),
            "perfect_guesses": stats.get("perfect_guesses", 0)
        }).execute()
        return True
    except Exception as e:
        print(f"Erreur sauvegarde stats joueur: {e}")
        return False

def is_player_guest(pseudo):
    """Vérifie si un joueur est invité"""
    return pseudo == "Invite" or pseudo == "invit" or not pseudo

def get_player_stats(pseudo):
    """Récupère toutes les stats d'un joueur"""
    try:
        result = supabase.table("player_game_stats")\
            .select("*")\
            .eq("pseudo", pseudo)\
            .execute()
        return result.data
    except Exception as e:
        print(f"Erreur récupération stats: {e}")
        return []

def get_player_history(pseudo, limit=10):
    """Récupère l'historique des parties d'un joueur"""
    try:
        result = supabase.table("player_game_stats")\
            .select("*, game_sessions(*)")\
            .eq("pseudo", pseudo)\
            .order("played_at", desc=True)\
            .limit(limit)\
            .execute()
        return result.data
    except Exception as e:
        print(f"Erreur récupération historique: {e}")
        return []

def get_game_session_details(session_id):
    """Récupère tous les détails d'une partie"""
    try:
        session = supabase.table("game_sessions")\
            .select("*")\
            .eq("id", session_id)\
            .single()\
            .execute()
        
        players = supabase.table("player_game_stats")\
            .select("*")\
            .eq("game_session_id", session_id)\
            .execute()
        
        rounds = supabase.table("round_details")\
            .select("*")\
            .eq("game_session_id", session_id)\
            .order("round_number")\
            .execute()
        
        return {
            "session": session.data,
            "players": players.data,
            "rounds": rounds.data
        }
    except Exception as e:
        print(f"Erreur récupération détails partie: {e}")
        return None