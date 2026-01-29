import sys, os
from supabase import create_client


def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)


def get_score_options_path():
    base_path = getattr(sys, '_MEIPASS', os.path.abspath("."))
    full_path = os.path.join(
        os.path.dirname(sys.executable if getattr(sys, 'frozen', False) else __file__),
        "score",
        "options.txt"
    )
    os.makedirs(os.path.dirname(full_path), exist_ok=True)
    return full_path


SUPABASE_URL = "https://dfrfhlvbckvakgtridzv.supabase.co"
SUPABASE_KEY = "sb_publishable_OEqgvVyKwJGXy5rV1H1Y8Q_kGL98num"

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)



def send_score(pseudo: str, mode: int, score: int):
   
    supabase.table("leaderboard").insert({
        "pseudo": pseudo,
        "mode": mode,
        "score": score
    }).execute()


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



def save_local_profile(pseudo):
    path = resource_path("GuessMyClass/profile/compte.txt")
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(pseudo)


def load_local_profile():
    try:
        with open(resource_path("GuessMyClass/profile/compte.txt"), "r", encoding="utf-8") as f:
            return f.read().strip()
    except FileNotFoundError:
        return ""
