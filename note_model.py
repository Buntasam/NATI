"""
Module de gestion des données pour l'application NotesAI.
"""
import os
import json
from datetime import datetime


class NoteModel:
    """Modèle de données pour gérer les notes."""

    def __init__(self):
        # Dictionnaire pour stocker les notes
        self.notes = {}
        self.current_note_id = None

        # Créer dossier de sauvegarde si nécessaire
        self.save_folder = os.path.join(os.path.expanduser("~"), "NotesAI")
        if not os.path.exists(self.save_folder):
            os.makedirs(self.save_folder)

        # Charger les notes existantes
        self.load_notes()

    def create_note(self):
        """Créer une nouvelle note."""
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        note_id = f"note_{timestamp}"

        self.notes[note_id] = {
            "title": "Nouvelle Note",
            "content": "",
            "created": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "modified": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "category": "Non classé"
        }

        self.current_note_id = note_id
        self.save_notes()
        return note_id

    def get_note(self, note_id):
        """Obtenir une note par son ID."""
        return self.notes.get(note_id)

    def update_note(self, note_id, title, content):
        """Mettre à jour une note existante."""
        if note_id in self.notes:
            self.notes[note_id]["title"] = title
            self.notes[note_id]["content"] = content
            self.notes[note_id]["modified"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            self.save_notes()
            return True
        return False

    def update_category(self, note_id, category):
        """Mettre à jour la catégorie d'une note."""
        if note_id in self.notes:
            self.notes[note_id]["category"] = category
            self.save_notes()
            return True
        return False

    def delete_note(self, note_id):
        """Supprimer une note."""
        if note_id in self.notes:
            del self.notes[note_id]
            self.save_notes()
            return True
        return False

    def get_all_notes(self):
        """Obtenir toutes les notes."""
        return self.notes

    def get_sorted_notes(self):
        """Obtenir les notes triées par date de modification."""
        return sorted(
            self.notes.items(),
            key=lambda x: x[1]["modified"],
            reverse=True
        )

    def search_notes(self, search_text):
        """Rechercher des notes par texte."""
        search_text = search_text.lower()
        results = []

        for note_id, note in self.notes.items():
            title = note["title"].lower()
            content = note["content"].lower()
            category = note["category"].lower()

            if (search_text in title or
                    search_text in content or
                    search_text in category):
                results.append((note_id, note))

        return sorted(
            results,
            key=lambda x: x[1]["modified"],
            reverse=True
        )

    def load_notes(self):
        """Charger les notes depuis le fichier."""
        notes_file = os.path.join(self.save_folder, "notes.json")

        if os.path.exists(notes_file):
            try:
                with open(notes_file, "r", encoding="utf-8") as f:
                    self.notes = json.load(f)
                return len(self.notes)
            except Exception as e:
                print(f"Erreur lors du chargement des notes: {str(e)}")
                return 0
        return 0

    def save_notes(self):
        """Sauvegarder les notes dans un fichier."""
        notes_file = os.path.join(self.save_folder, "notes.json")

        try:
            with open(notes_file, "w", encoding="utf-8") as f:
                json.dump(self.notes, f, ensure_ascii=False, indent=2)
            return True
        except Exception as e:
            print(f"Erreur lors de la sauvegarde des notes: {str(e)}")
            return False