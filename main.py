"""
Script principal pour lancer l'application NotesAI.
Ce fichier intègre tous les composants et lance l'interface utilisateur.
"""
import tkinter as tk
from tkinter import ttk

from note_model import NoteModel
from ai_service import AIService
from notes_ui import NotesUI


def show_disclaimer(root):
    """Affiche une fenêtre de disclaimer avant le lancement de l'application."""
    disclaimer = tk.Toplevel(root)
    disclaimer.title("Disclaimer")
    disclaimer.geometry("800x600")
    disclaimer.grab_set()  # Rendre la fenêtre modale

    label = tk.Label(
        disclaimer,
        text = (
            "⚠️ AVERTISSEMENT\n\n"
            "NotesAI est une application en cours de développement. En l'utilisant, vous acceptez les conditions suivantes :\n\n"
            "- L'utilisation de l'intelligence artificielle (via Ollama) peut entraîner des temps de réponse lents si votre machine n'est pas suffisamment puissante ou si vous n'utilisez pas de clé API dédiée.\n"
                "- L'application nécessite l'installation de l'outil Ollama, ainsi que le téléchargement d'un modèle compatible (ex : llama3, mistral, etc.). Vous devez également laisser Ollama ouvert en arrière-plan pendant l'utilisation de NotesAI.\n"
            "- Aucune garantie de performance ou de fiabilité n'est assurée à ce stade.\n"
            "- Nous déclinons toute responsabilité en cas de perte de données, dysfonctionnement, ou tout autre incident lié à l'utilisation de cette application.\n\n"
            "En cliquant sur \"Accepter\", vous reconnaissez avoir pris connaissance de ces informations et acceptez de continuer à vos propres risques."
            " "
            ),

        wraplength=350
    )
    label.pack(pady=20)

    def accept():
        disclaimer.destroy()

    def decline():
        disclaimer.destroy()
        root.destroy()  # Ferme l'app si refusé

    button_frame = tk.Frame(disclaimer)
    button_frame.pack(pady=10)

    accept_btn = tk.Button(button_frame, text="Accepter", command=accept)
    accept_btn.pack(side=tk.LEFT, padx=10)

    decline_btn = tk.Button(button_frame, text="Refuser", command=decline)
    decline_btn.pack(side=tk.LEFT, padx=10)

    # Attendre que l'utilisateur interagisse avec le disclaimer
    root.wait_window(disclaimer)


def main():
    """Fonction principale pour lancer l'application."""
    # Créer la fenêtre principale
    root = tk.Tk()
    root.withdraw()  # Cacher la fenêtre principale au début

    # Afficher le disclaimer
    show_disclaimer(root)

    # Si l'utilisateur a accepté, continuer
    if not root.winfo_exists():
        return  # L'utilisateur a fermé/refusé l'application

    root.deiconify()  # Afficher la fenêtre principale
    root.title("NotesAI - Bloc-notes intelligent avec IA")

    # Configurer le style ttk
    style = ttk.Style()
    style.configure("TCombobox", padding=5)

    # Initialiser les composants
    note_model = NoteModel()
    ai_service = AIService()

    # Créer l'interface
    notes_ui = NotesUI(root, note_model, ai_service)

    # Lancer la boucle principale
    root.mainloop()


if __name__ == "__main__":
    main()
