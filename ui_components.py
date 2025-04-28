"""
Module de composants d'interface utilisateur pour l'application NotesAI.
"""
import tkinter as tk
from tkinter import scrolledtext, messagebox, ttk


class ResultWindow:
    """Fenêtre de résultat pour afficher des contenus générés par l'IA."""

    def __init__(self, root, title, content, theme):
        """
        Initialiser une fenêtre de résultat.

        Args:
            root (tk.Tk): La fenêtre racine
            title (str): Le titre de la fenêtre
            content (str): Le contenu à afficher
            theme (dict): Le thème actuel
        """
        self.window = tk.Toplevel(root)
        self.window.title(title)
        self.window.geometry("600x500")
        self.window.configure(bg=theme["bg"])

        # Cadre principal avec marge
        main_frame = tk.Frame(self.window, bg=theme["bg"], padx=20, pady=20)
        main_frame.pack(fill=tk.BOTH, expand=True)

        # Titre
        title_label = tk.Label(main_frame, text=title, font=("Arial", 16, "bold"),
                               bg=theme["bg"], fg=theme["fg"])
        title_label.pack(anchor=tk.W, pady=(0, 15))

        # Cadre pour la zone de texte
        text_frame = tk.Frame(main_frame, bg=theme["border"], padx=1, pady=1)
        text_frame.pack(fill=tk.BOTH, expand=True)

        # Zone de texte
        self.text_area = scrolledtext.ScrolledText(text_frame, wrap=tk.WORD,
                                                   font=("Arial", 12),
                                                   bg=theme["text_bg"],
                                                   fg=theme["text_fg"],
                                                   relief=tk.FLAT, padx=10, pady=10)
        self.text_area.pack(fill=tk.BOTH, expand=True)
        self.text_area.insert(tk.END, content)

        # Boutons
        button_frame = tk.Frame(main_frame, bg=theme["bg"], pady=15)
        button_frame.pack(fill=tk.X)

        copy_button = tk.Button(button_frame, text="Copier", relief=tk.FLAT,
                                bg=theme["button_bg"], fg=theme["button_fg"],
                                padx=10, pady=5, command=self.copy_to_clipboard)
        copy_button.pack(side=tk.LEFT, padx=5)

        close_button = tk.Button(button_frame, text="Fermer", relief=tk.FLAT,
                                 bg=theme["button_bg"], fg=theme["button_fg"],
                                 padx=10, pady=5, command=self.window.destroy)
        close_button.pack(side=tk.RIGHT, padx=5)

        # Rendre la fenêtre modale
        self.window.transient(root)
        self.window.grab_set()

    def copy_to_clipboard(self):
        """Copier le contenu dans le presse-papiers."""
        content = self.text_area.get(1.0, tk.END).strip()
        self.window.clipboard_clear()
        self.window.clipboard_append(content)
        messagebox.showinfo("Information", "Copié dans le presse-papiers")


def create_custom_dialog(root, title, message, theme):
    """
    Créer une boîte de dialogue personnalisée.

    Args:
        root (tk.Tk): La fenêtre racine
        title (str): Le titre de la boîte de dialogue
        message (str): Le message à afficher
        theme (dict): Le thème actuel

    Returns:
        bool: True si l'utilisateur a cliqué sur Oui, False sinon
    """
    dialog = tk.Toplevel(root)
    dialog.title(title)
    dialog.geometry("400x200")
    dialog.configure(bg=theme["bg"])
    dialog.resizable(False, False)

    # Rendre la boîte de dialogue modale
    dialog.transient(root)
    dialog.grab_set()

    # Centrer la boîte de dialogue
    dialog.update_idletasks()
    width = dialog.winfo_width()
    height = dialog.winfo_height()
    x = (root.winfo_width() // 2) - (width // 2) + root.winfo_x()
    y = (root.winfo_height() // 2) - (height // 2) + root.winfo_y()
    dialog.geometry(f"+{x}+{y}")

    # Contenu
    main_frame = tk.Frame(dialog, bg=theme["bg"], padx=20, pady=20)
    main_frame.pack(fill=tk.BOTH, expand=True)

    message_label = tk.Label(main_frame, text=message, wraplength=350,
                             font=("Arial", 12), bg=theme["bg"], fg=theme["fg"])
    message_label.pack(pady=(10, 20))

    # Boutons
    button_frame = tk.Frame(main_frame, bg=theme["bg"])
    button_frame.pack(fill=tk.X, pady=(0, 10))

    result = [False]  # Variable pour stocker le résultat

    def on_yes():
        result[0] = True
        dialog.destroy()

    def on_no():
        result[0] = False
        dialog.destroy()

    yes_button = tk.Button(button_frame, text="Oui", relief=tk.FLAT,
                           bg=theme["accent"], fg="white", padx=15, pady=5,
                           command=on_yes)
    yes_button.pack(side=tk.RIGHT, padx=5)

    no_button = tk.Button(button_frame, text="Non", relief=tk.FLAT,
                          bg=theme["button_bg"], fg=theme["button_fg"], padx=15, pady=5,
                          command=on_no)
    no_button.pack(side=tk.RIGHT, padx=5)

    # Attendre que l'utilisateur ferme la boîte de dialogue
    dialog.wait_window()

    return result[0]