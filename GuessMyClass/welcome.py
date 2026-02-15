import sys, os
import pygame
import customtkinter as ctk
from supabase import create_client
from utils import resource_path

# Initialisation Supabase
SUPABASE_URL = "https://dfrfhlvbckvakgtridzv.supabase.co"
SUPABASE_KEY = "sb_publishable_OEqgvVyKwJGXy5rV1H1Y8Q_kGL98num"
supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

def save_local_profile(pseudo):
    """Sauvegarde le pseudo localement"""
    path = resource_path("GuessMyClass/profile/compte.txt")
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(pseudo)

def load_local_profile():
    """Charge le pseudo local"""
    try:
        with open(resource_path("GuessMyClass/profile/compte.txt"), "r", encoding="utf-8") as f:
            return f.read().strip()
    except FileNotFoundError:
        return ""

def check_or_create_profile(pseudo):
    """Vérifie si le pseudo existe, sinon le crée automatiquement"""
    try:
        result = supabase.table("leaderboard")\
            .select("pseudo")\
            .eq("pseudo", pseudo)\
            .limit(1)\
            .execute()
        
        if result.data and len(result.data) > 0:
            print(f"✅ Connexion: {pseudo}")
            return True
        else:
            supabase.table("leaderboard").insert({
                "pseudo": pseudo,
                "mode": 5,
                "score": 0
            }).execute()
            print(f"✅ Compte créé: {pseudo}")
            return True
            
    except Exception as e:
        print(f"Erreur: {e}")
        return False

def open_login_window():
    """Fenêtre unique pour se connecter OU créer un compte"""
    result = [None]
    
    root = ctk.CTk()
    root.title("Connexion")
    root.geometry("350x250")  # ✅ Plus petite : 350x250 au lieu de 400x300
    root.configure(fg_color="#CDE4E2")
    root.resizable(False, False)  # Empêche le redimensionnement
    
    root.lift()
    root.focus_force()
    root.attributes('-topmost', True)
    root.after(100, lambda: root.attributes('-topmost', False))
    
    # Titre plus petit
    title = ctk.CTkLabel(root, text="Connexion", font=("Arial", 20, "bold"))
    title.pack(pady=15)
    
    # Info plus compacte
    info_label = ctk.CTkLabel(
        root, 
        text="Entrez votre pseudo", 
        font=("Arial", 11),
        text_color="#555555"
    )
    info_label.pack(pady=3)
    
    # Champ pseudo
    pseudo_label = ctk.CTkLabel(root, text="Pseudo:", font=("Arial", 14))
    pseudo_label.pack(pady=3)
    pseudo_entry = ctk.CTkEntry(root, width=250, font=("Arial", 13))
    pseudo_entry.pack(pady=3)
    pseudo_entry.focus()
    
    # Message d'erreur
    message_label = ctk.CTkLabel(root, text="", font=("Arial", 11))
    message_label.pack(pady=3)
    
    def validate_and_login():
        pseudo = pseudo_entry.get().strip()
        
        if not pseudo:
            message_label.configure(text="Le pseudo ne peut pas être vide", text_color="red")
            return
        
        if len(pseudo) < 3:
            message_label.configure(text="Minimum 3 caractères", text_color="red")
            return
        
        if len(pseudo) > 20:
            message_label.configure(text="Maximum 20 caractères", text_color="red")
            return
        
        success = check_or_create_profile(pseudo)
        
        if success:
            save_local_profile(pseudo)
            result[0] = True
            root.destroy()
        else:
            message_label.configure(text="Erreur de connexion", text_color="red")
    
    # Boutons plus compacts
    validate_btn = ctk.CTkButton(
        root, 
        text="Valider", 
        command=validate_and_login,
        fg_color="#FF9100",
        hover_color="#C35500",
        font=("Arial", 14),
        width=150,
        height=35
    )
    validate_btn.pack(pady=10)
    
    cancel_btn = ctk.CTkButton(
        root, 
        text="Annuler", 
        command=root.destroy,
        fg_color="#888888",
        hover_color="#666666",
        font=("Arial", 14),
        width=150,
        height=35
    )
    cancel_btn.pack(pady=3)
    
    root.bind('<Return>', lambda e: validate_and_login())
    
    root.mainloop()
    return result[0]

def welcome_display():
    """Écran d'accueil simplifié"""
    screen = pygame.display.get_surface()
    w, h = screen.get_size()
    
    font_title = pygame.font.Font(resource_path("GuessMyClass/font/MightySouly.ttf"), 80)
    font_subtitle = pygame.font.Font(resource_path("GuessMyClass/font/MightySouly.ttf"), 50)
    font_button = pygame.font.Font(resource_path("GuessMyClass/font/MightySouly.ttf"), 30)  # ✅ Police plus petite pour le texte long
    
    bg_color = (205, 228, 226)
    title_color = (255, 255, 255)
    subtitle_color = (255, 255, 255)
    button_login_color = (180, 130, 230)
    button_login_hover = (150, 100, 200)
    button_guest_color = (180, 180, 180)
    button_guest_hover = (150, 150, 150)
    
    button_w, button_h = 350, 80
    button_login_rect = pygame.Rect(w//2 - 400, h//2 + 100, button_w, button_h)
    button_guest_rect = pygame.Rect(w//2 + 50, h//2 + 100, button_w, button_h)
    
    login_was_pressed = False
    guest_was_pressed = False
    
    running = True
    clock = pygame.time.Clock()
    
    while running:
        mouse_pos = pygame.mouse.get_pos()
        mouse_pressed = pygame.mouse.get_pressed()[0]
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return 'hell'
        
        login_hovered = button_login_rect.collidepoint(mouse_pos)
        guest_hovered = button_guest_rect.collidepoint(mouse_pos)
        
        if not mouse_pressed:
            # ===== BOUTON CRÉER/SE CONNECTER =====
            if login_hovered and login_was_pressed:
                login_was_pressed = False
                
                pygame.event.clear()
                result = open_login_window()
                
                if result:
                    pygame.time.delay(100)
                    return 'home'
            
            # ===== BOUTON INVITÉ =====
            if guest_hovered and guest_was_pressed:
                guest_was_pressed = False
                save_local_profile("Invite\ninvit")
                return 'home'
        
        if mouse_pressed:
            if login_hovered:
                login_was_pressed = True
            if guest_hovered:
                guest_was_pressed = True
        
        # ===== DESSIN =====
        screen.fill(bg_color)
        
        title_text = font_title.render("Bienvenue sur GMC !", True, title_color)
        title_rect = title_text.get_rect(center=(w//2, 100))
        title_bg = pygame.Rect(title_rect.x - 20, title_rect.y - 10, title_rect.width + 40, title_rect.height + 20)
        pygame.draw.rect(screen, (104, 180, 229), title_bg, border_radius=15)
        screen.blit(title_text, title_rect)
        
        subtitle_text = font_subtitle.render("Que voulez-vous faire ?", True, subtitle_color)
        subtitle_rect = subtitle_text.get_rect(center=(w//2, 250))
        subtitle_bg = pygame.Rect(subtitle_rect.x - 20, subtitle_rect.y - 10, subtitle_rect.width + 40, subtitle_rect.height + 20)
        pygame.draw.rect(screen, (150, 180, 220), subtitle_bg, border_radius=15)
        screen.blit(subtitle_text, subtitle_rect)
        
        # ✅ Bouton "Créer/Se connecter"
        color_login = button_login_hover if login_hovered else button_login_color
        pygame.draw.rect(screen, color_login, button_login_rect, border_radius=15)
        login_text = font_button.render("Créer/Se connecter", True, (255, 255, 255))
        login_text_rect = login_text.get_rect(center=button_login_rect.center)
        screen.blit(login_text, login_text_rect)
        
        # Bouton "Jouer sans compte"
        color_guest = button_guest_hover if guest_hovered else button_guest_color
        pygame.draw.rect(screen, color_guest, button_guest_rect, border_radius=15)
        guest_text = font_button.render("Jouer sans compte", True, (255, 255, 255))
        guest_text_rect = guest_text.get_rect(center=button_guest_rect.center)
        screen.blit(guest_text, guest_text_rect)
        
        pygame.display.flip()
        clock.tick(60)
    
    return None