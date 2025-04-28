"""
Module de gestion des thèmes pour l'application NotesAI.
"""
import tkinter as tk


class ThemeManager:
    """Gestionnaire de thèmes pour l'application NotesAI."""

    def __init__(self):
        # Couleurs pour le thème clair
        self.light_theme = {
            "bg": "#f5f5f5",
            "fg": "#333333",
            "accent": "#333333",
            "accent_hover": "#333333",
            "text_bg": "#ffffff",
            "text_fg": "#333333",
            "border": "#dddddd",
            "highlight": "#e6f3fb",
            "status_bg": "#f5f5f5",
            "button_bg": "#e1e1e1",
            "button_fg": "#333333",
            "sidebar_bg": "#f0f0f0",
            "note_selected": "#ddeeff"
        }

                # Couleurs pour le thème sombre
        self.dark_theme = {
    "bg": "#000000",             # Fond principal : noir absolu
    "fg": "#e0e0e0",             # Texte principal : gris clair
    "accent": "#111111",         # Boutons/headers : presque noir
    "accent_hover": "#222222",   # Survols : légèrement plus clair
    "text_bg": "#000000",        # Fond de texte : noir
    "text_fg": "#e0e0e0",        # Texte dans les zones d’édition : gris clair
    "border": "#222222",         # Bordures : très foncées
    "highlight": "#1a1a1a",      # Survols & sélections
    "status_bg": "#000000",      # Barre de statut : noir
    "button_bg": "#111111",      # Fond des boutons : noir doux
    "button_fg": "#f5f5f5",      # Texte des boutons : presque blanc
    "sidebar_bg": "#000000",     # Sidebar à gauche : noir total
    "note_selected": "#1a1a1a"   # Note sélectionnée : gris très foncé
}



        # Thème actif
        self.current_theme = self.light_theme
    def get_theme(self):
        """Obtenir le thème actuel."""
        return self.current_theme

    def toggle_theme(self):
        """Basculer entre les thèmes clair et sombre."""
        if self.current_theme == self.light_theme:
            self.current_theme = self.dark_theme
        else:
            self.current_theme = self.light_theme
        return self.current_theme


class StyledButton(tk.Button):
    """Bouton stylisé avec effets de survol."""

    def __init__(self, master=None, theme_manager=None, **kwargs):
        self.theme_manager = theme_manager
        self.hover = False

        theme = theme_manager.get_theme()
        kwargs.setdefault("bg", theme["button_bg"])
        kwargs.setdefault("fg", theme["button_fg"])
        kwargs.setdefault("relief", tk.FLAT)
        kwargs.setdefault("borderwidth", 0)
        kwargs.setdefault("padx", 10)
        kwargs.setdefault("pady", 5)

        super().__init__(master, **kwargs)

        self.bind("<Enter>", self.on_enter)
        self.bind("<Leave>", self.on_leave)

    def on_enter(self, e):
        """Effet lors du survol."""
        self.hover = True
        theme = self.theme_manager.get_theme()
        self.config(bg=theme["accent"], fg="white")

    def on_leave(self, e):
        """Effet lors de la sortie du survol."""
        self.hover = False
        theme = self.theme_manager.get_theme()
        self.config(bg=theme["button_bg"], fg=theme["button_fg"])

    def update_style(self, theme):
        """Mettre à jour le style du bouton."""
        if self.hover:
            
            self.config(bg=theme["accent"], fg="white")
        else:
            self.config(bg=theme["button_bg"], fg=theme["button_fg"])