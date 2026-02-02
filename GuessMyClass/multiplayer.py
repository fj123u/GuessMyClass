import random
import string
from supabase import create_client
import time

SUPABASE_URL = "https://dfrfhlvbckvakgtridzv.supabase.co"
SUPABASE_KEY = "sb_publishable_OEqgvVyKwJGXy5rV1H1Y8Q_kGL98num"
supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

def generate_room_code():
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))

def create_room(pseudo, mode=5):
    room_code = generate_room_code()
    try:
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
        result = supabase.table("game_rooms")\
            .select("*")\
            .eq("room_code", room_code)\
            .eq("status", "waiting")\
            .single()\
            .execute()
        
        if not result.data:
            return None
        
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