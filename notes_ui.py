"""
Module d'interface utilisateur principale pour l'application NotesAI.
"""
import tkinter as tk
from tkinter import scrolledtext, ttk, messagebox
import os
import json

from theme_manager import ThemeManager, StyledButton
from ui_components import ResultWindow, create_custom_dialog

class NotesUI:
    """Interface utilisateur principale pour l'application NotesAI."""

    def __init__(self, root, note_model, ai_service):
        """
        Initialiser l'interface utilisateur.

        Args:
            root (tk.Tk): La fenêtre racine
            note_model (NoteModel): Le modèle de données pour les notes
            ai_service (AIService): Le service d'IA
        """
        self.root = root
        self.note_model = note_model
        self.ai_service = ai_service

        # Configuration de base
        self.root.title("NotesAI - Bloc-notes intelligent")
        self.root.geometry("1200x800")

        
        # Gestionnaire de thème
        self.theme_manager = ThemeManager()
        self.theme = self.theme_manager.get_theme()

        # Widgets importants à accéder plus tard
        self.title_entry = None
        self.text_area = None
        self.note_listbox = None
        self.category_label = None
        self.date_label = None
        self.search_var = None
        self.status_var = None

        # Créer l'interface
        self.create_ui()
        self.apply_theme()

        # Charger les notes existantes
        self.refresh_note_list()

    def toggle_theme_and_update_logo(self):
        self.toggle_theme()


    def create_ui(self):
    

        #SAM
        """Créer l'interface utilisateur."""
        # Configurer la couleur de fond
        self.root.configure(bg=self.theme["bg"])

        # Créer un cadre pour le header
        header_frame = tk.Frame(self.root, bg=self.theme["accent"], padx=10, pady=5)
        header_frame.pack(fill=tk.X)

        #title_label = tk.Label(header_frame, text="NotesAI",
                              #font=("Arial", 16, "bold"),
                             # bg=self.theme["accent"], fg="white")
        #title_label.pack(side=tk.LEFT, padx=5)


        # Créer un cadre principal
        main_frame = tk.Frame(self.root, bg=self.theme["bg"])
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Séparateur entre liste et zone d'édition
        paned_window = tk.PanedWindow(main_frame, orient=tk.HORIZONTAL,
                                     bg=self.theme["border"], sashwidth=2)
        paned_window.pack(fill=tk.BOTH, expand=True)

        # Cadre gauche pour la liste de notes
        left_frame = tk.Frame(paned_window, width=300, bg=self.theme["sidebar_bg"])
        paned_window.add(left_frame, width=300)

        # Cadre droit pour l'édition
        right_frame = tk.Frame(paned_window, bg=self.theme["bg"])
        paned_window.add(right_frame)

        # Zone de recherche avec style
        search_frame = tk.Frame(left_frame, bg=self.theme["sidebar_bg"], pady=10)
        search_frame.pack(fill=tk.X)

        search_icon_label = tk.Label(search_frame, text="🔍", bg=self.theme["sidebar_bg"],
                                    fg=self.theme["fg"])
        search_icon_label.pack(side=tk.LEFT, padx=(5, 0))

        self.search_var = tk.StringVar()
        self.search_var.trace("w", self.filter_notes)
        search_entry = tk.Entry(search_frame, textvariable=self.search_var,
                               font=("Arial", 11), bg=self.theme["text_bg"],
                               fg=self.theme["text_fg"], relief=tk.FLAT,
                               highlightthickness=1, highlightbackground=self.theme["border"])
        search_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)

        # Étiquette "Mes Notes"
        notes_label = tk.Label(left_frame, text="Mes Notes", font=("Arial", 12, "bold"),
                              bg=self.theme["sidebar_bg"], fg=self.theme["fg"])
        notes_label.pack(anchor=tk.W, padx=10, pady=(10, 5))

        # Liste des notes avec custom frame
        list_frame = tk.Frame(left_frame, bg=self.theme["sidebar_bg"], padx=10)
        list_frame.pack(fill=tk.BOTH, expand=True)

        self.note_listbox = tk.Listbox(list_frame, selectmode=tk.SINGLE,
                                     bg=self.theme["text_bg"], fg=self.theme["text_fg"],
                                     font=("Arial", 11), relief=tk.FLAT,
                                     highlightthickness=1,
                                     highlightbackground=self.theme["border"],
                                     selectbackground=self.theme["note_selected"],
                                     selectforeground=self.theme["text_fg"])
        self.note_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        scrollbar = tk.Scrollbar(list_frame, orient=tk.VERTICAL,
                               command=self.note_listbox.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.note_listbox.config(yscrollcommand=scrollbar.set)

        # Boutons d'actions pour les notes
        button_frame = tk.Frame(left_frame, bg=self.theme["sidebar_bg"], pady=10)
        button_frame.pack(fill=tk.X)

        self.new_button = StyledButton(button_frame, self.theme_manager,
                                     text="+ Nouvelle Note", command=self.new_note)
        self.new_button.pack(side=tk.LEFT, padx=5)

        self.delete_button = StyledButton(button_frame, self.theme_manager,
                                        text="🗑️ Supprimer", command=self.delete_note)
        self.delete_button.pack(side=tk.LEFT, padx=5)

        # Zone d'édition avec style moderne
        edit_frame = tk.Frame(right_frame, bg=self.theme["bg"], padx=20, pady=10)
        edit_frame.pack(fill=tk.BOTH, expand=True)

        # Titre de la note
        title_frame = tk.Frame(edit_frame, bg=self.theme["bg"], pady=10)
        title_frame.pack(fill=tk.X)

        self.title_entry = tk.Entry(title_frame, font=("Arial", 16, "bold"),
                                   bg=self.theme["bg"], fg=self.theme["fg"],
                                   relief=tk.FLAT, highlightthickness=0,
                                   insertbackground=self.theme["fg"])
        self.title_entry.pack(fill=tk.X, expand=True)
        self.title_entry.insert(0, "Sélectionnez une note...")

        # Séparateur sous le titre
        title_separator = tk.Frame(edit_frame, height=1, bg=self.theme["border"])
        title_separator.pack(fill=tk.X, pady=(0, 10))

        # Catégorie et date
        info_frame = tk.Frame(edit_frame, bg=self.theme["bg"])
        info_frame.pack(fill=tk.X, pady=(0, 10))

        self.category_label = tk.Label(info_frame, text="Catégorie: -",
                                      font=("Arial", 10), bg=self.theme["bg"],
                                      fg=self.theme["accent"])
        self.category_label.pack(side=tk.LEFT)

        self.date_label = tk.Label(info_frame, text="", font=("Arial", 10),
                                  bg=self.theme["bg"], fg=self.theme["fg"])
        self.date_label.pack(side=tk.RIGHT)

        # Zone de texte avec cadre visuel
        text_frame = tk.Frame(edit_frame, bg=self.theme["border"], padx=1, pady=1)
        text_frame.pack(fill=tk.BOTH, expand=True)

        self.text_area = scrolledtext.ScrolledText(text_frame, wrap=tk.WORD,
                                                 font=("Arial", 12),
                                                 bg=self.theme["text_bg"],
                                                 fg=self.theme["text_fg"],
                                                 insertbackground=self.theme["fg"],
                                                 selectbackground=self.theme["accent"],
                                                 relief=tk.FLAT, padx=10, pady=10)
        self.text_area.pack(fill=tk.BOTH, expand=True)

        # Barre d'outils pour IA
        ai_frame = tk.Frame(edit_frame, bg=self.theme["bg"], pady=15)
        ai_frame.pack(fill=tk.X)

        # Modèle avec style dropdown
        model_label = tk.Label(ai_frame, text="Modèle:", bg=self.theme["bg"],
                              fg=self.theme["fg"])
        model_label.pack(side=tk.LEFT, padx=(0, 5))

        ai_models = [
            "mistral (local)",
            "llama2 (local)",
            "gemma (local)",
            "phi (local)",
            "gpt-3.5-turbo (openai)",
            "claude-3-haiku-20240307 (anthropic)"
        ]

        self.model_var = tk.StringVar(value=self.ai_service.get_model())
        model_dropdown = ttk.Combobox(ai_frame, textvariable=self.model_var, values=ai_models,
                                    width=10, style="TCombobox")
        model_dropdown.pack(side=tk.LEFT, padx=(0, 10))
        model_dropdown.bind("<<ComboboxSelected>>", self.update_model)

        # Boutons AI stylisés
        self.correct_button = StyledButton(ai_frame, self.theme_manager,
                                         text="✓ Corriger",
                                         command=lambda: self.process_with_ai("correction"))
        self.correct_button.pack(side=tk.LEFT, padx=5)

        self.summarize_button = StyledButton(ai_frame, self.theme_manager,
                                           text="📝 Résumer",
                                           command=lambda: self.process_with_ai("resume"))
        self.summarize_button.pack(side=tk.LEFT, padx=5)

        self.categorize_button = StyledButton(ai_frame, self.theme_manager,
                                            text="🏷️ Catégoriser",
                                            command=lambda: self.process_with_ai("categorie"))
        self.categorize_button.pack(side=tk.LEFT, padx=5)

        
        # Bouton de thème
        self.theme_button = StyledButton(ai_frame, self.theme_manager, text="Mode Sombre",
                                        command=self.toggle_theme_and_update_logo)
        self.theme_button.pack(side=tk.RIGHT, padx=5)

        self.prompt_config_button = StyledButton(ai_frame, self.theme_manager,
        text="⚙️ Prompts IA",
        command=self.open_prompt_editor)
        self.prompt_config_button.pack(side=tk.RIGHT, padx=5)



        # Pied de page avec statut
        status_frame = tk.Frame(self.root, bg=self.theme["status_bg"], padx=10, pady=5)
        status_frame.pack(side=tk.BOTTOM, fill=tk.X)

        self.status_var = tk.StringVar(value="Prêt")
        status_label = tk.Label(status_frame, textvariable=self.status_var,
                               bg=self.theme["status_bg"], fg=self.theme["fg"],
                               anchor=tk.W)
        status_label.pack(side=tk.LEFT, fill=tk.X, expand=True)

        # Binds
        self.note_listbox.bind('<<ListboxSelect>>', self.load_selected_note)
        self.text_area.bind('<KeyRelease>', self.auto_save)
        self.title_entry.bind('<KeyRelease>', self.auto_save)

        self.api_key_button = StyledButton(ai_frame, self.theme_manager,
                                   text="🔑 Clé API",
                                   command=self.open_api_key_dialog)
        self.api_key_button.pack(side=tk.RIGHT, padx=5)


    def toggle_theme(self):
        """Basculer entre les thèmes clair et sombre."""
        self.theme = self.theme_manager.toggle_theme()
        self.apply_theme()

        # Mettre à jour le texte du bouton
        if self.theme == self.theme_manager.dark_theme:
            self.theme_button.config(text="Mode Clair")
        else:
            self.theme_button.config(text="Mode Sombre")

    def apply_theme(self):
        """Appliquer le thème actuel à tous les éléments."""
        self.root.configure(bg=self.theme["bg"])

        # Mettre à jour les widgets
        self.theme_button.update_style(self.theme)
        self.new_button.update_style(self.theme)
        self.delete_button.update_style(self.theme)
        self.correct_button.update_style(self.theme)
        self.summarize_button.update_style(self.theme)
        self.categorize_button.update_style(self.theme)

        # Mettre à jour le style ttk
        style = ttk.Style()
        style.configure("TCombobox", fieldbackground=self.theme["text_bg"],
                      background=self.theme["text_bg"], foreground=self.theme["text_fg"])

        # Mettre à jour récursivement tous les widgets
        for widget in self.root.winfo_children():
            self.update_widget_colors(widget)

    def update_widget_colors(self, parent):
        """Mettre à jour récursivement les couleurs des widgets."""
        for widget in parent.winfo_children():
            try:
                if isinstance(widget, tk.Frame):
                    if "sidebar_bg" in str(widget):
                        widget.configure(bg=self.theme["sidebar_bg"])
                    elif "status_bg" in str(widget):
                        widget.configure(bg=self.theme["status_bg"])
                    elif "border" in str(widget):
                        widget.configure(bg=self.theme["border"])
                    else:
                        widget.configure(bg=self.theme["bg"])
                    self.update_widget_colors(widget)
                elif isinstance(widget, tk.Label):
                    parent_bg = self.theme["bg"]
                    if "sidebar" in str(parent):
                        parent_bg = self.theme["sidebar_bg"]
                    elif "header" in str(parent):
                        parent_bg = self.theme["accent"]
                        widget.configure(bg=parent_bg, fg="white")
                    elif "status" in str(parent):
                        parent_bg = self.theme["status_bg"]
                        widget.configure(bg=parent_bg, fg=self.theme["fg"])
                    elif "category" in str(widget):
                        widget.configure(bg=self.theme["bg"], fg=self.theme["accent"])
                    else:
                        widget.configure(bg=parent_bg, fg=self.theme["fg"])
                elif isinstance(widget, tk.Listbox):
                    widget.configure(
                        bg=self.theme["text_bg"],
                        fg=self.theme["text_fg"],
                        selectbackground=self.theme["note_selected"],
                        selectforeground=self.theme["text_fg"]
                    )
                elif isinstance(widget, scrolledtext.ScrolledText):
                    widget.configure(
                        bg=self.theme["text_bg"],
                        fg=self.theme["text_fg"],
                        insertbackground=self.theme["fg"],
                        selectbackground=self.theme["accent"]
                    )
                elif isinstance(widget, tk.Entry):
                    widget.configure(
                        bg=self.theme["text_bg"] if "search" in str(widget) else self.theme["bg"],
                        fg=self.theme["text_fg"],
                        insertbackground=self.theme["fg"]
                    )
            except Exception:
                # Ignorer les widgets qui ne peuvent pas être configurés
                pass

    def new_note(self):
        """Créer une nouvelle note."""
        note_id = self.note_model.create_note()
        self.note_model.current_note_id = note_id
        self.refresh_note_list()

        # Sélectionner la nouvelle note
        items = self.note_listbox.get(0, tk.END)
        for i, item in enumerate(items):
            if item.startswith("Nouvelle Note"):
                self.note_listbox.selection_set(i)
                self.note_listbox.see(i)
                break

        # Mettre à jour l'interface
        self.load_note_content(note_id)
        self.status_var.set("Nouvelle note créée")

    def load_selected_note(self, event=None):
        """Charger la note sélectionnée."""
        if not self.note_listbox.curselection():
            return

        index = self.note_listbox.curselection()[0]
        display_title = self.note_listbox.get(index)

        # Trouver la note correspondante
        for note_id, note in self.note_model.get_all_notes().items():
            list_title = f"{note['title']} - {note['category']}"
            if list_title == display_title:
                self.note_model.current_note_id = note_id
                self.load_note_content(note_id)
                self.status_var.set(f"Note chargée - Modifiée le {note['modified']}")
                break

    def load_note_content(self, note_id):
        """Charger le contenu d'une note dans l'interface."""
        note = self.note_model.get_note(note_id)
        if note:
            self.title_entry.delete(0, tk.END)
            self.title_entry.insert(0, note["title"])

            self.text_area.delete(1.0, tk.END)
            self.text_area.insert(tk.END, note["content"])

            self.update_info_labels(note)

    def update_info_labels(self, note=None):
        """Mettre à jour les étiquettes d'information."""
        if not note and self.note_model.current_note_id:
            note = self.note_model.get_note(self.note_model.current_note_id)

        if note:
            self.category_label.config(text=f"Catégorie: {note['category']}")
            self.date_label.config(text=f"Créée le {note['created']} | Modifiée le {note['modified']}")
        else:
            self.category_label.config(text="Catégorie: -")
            self.date_label.config(text="")

    def auto_save(self, event=None):
        """Sauvegarder automatiquement lors de l'édition."""
        if self.note_model.current_note_id:
            title = self.title_entry.get().strip()
            content = self.text_area.get(1.0, tk.END).strip()

            if not title:
                title = "Sans titre"

            self.note_model.update_note(self.note_model.current_note_id, title, content)
            self.update_info_labels()
            self.refresh_note_list()
            self.status_var.set(f"Note sauvegardée - {tk.StringVar().get()}")

    def delete_note(self):
        """Supprimer la note sélectionnée."""
        if not self.note_model.current_note_id:
            messagebox.showinfo("Information", "Aucune note sélectionnée")
            return

        # Demander confirmation
        confirm = create_custom_dialog(
            self.root,
            "Confirmation",
            "Voulez-vous vraiment supprimer cette note?",
            self.theme
        )

        if confirm:
            self.note_model.delete_note(self.note_model.current_note_id)
            self.refresh_note_list()

            self.note_model.current_note_id = None
            self.title_entry.delete(0, tk.END)
            self.title_entry.insert(0, "Sélectionnez une note...")
            self.text_area.delete(1.0, tk.END)
            self.update_info_labels()
            self.status_var.set("Note supprimée")

    def filter_notes(self, *args):
        """Filtrer les notes par recherche."""
        self.refresh_note_list()

    def refresh_note_list(self):
        """Mettre à jour la liste des notes."""
        self.note_listbox.delete(0, tk.END)

        search_text = self.search_var.get().lower() if self.search_var else ""

        if search_text:
            notes = self.note_model.search_notes(search_text)
        else:
            notes = self.note_model.get_sorted_notes()

        for note_id, note in notes:
            display_text = f"{note['title']} - {note['category']}"
            self.note_listbox.insert(tk.END, display_text)

            # Si c'est la note actuelle, la sélectionner
            if note_id == self.note_model.current_note_id:
                self.note_listbox.selection_set(tk.END)

    def update_model(self, event=None):
        """Mettre à jour le modèle d'IA sélectionné."""
        selected = self.model_var.get()
        
        # Extraire nom + fournisseur
        if "(openai)" in selected:
            model_name = selected.split(" (")[0]
            self.ai_service.set_model(model_name, provider="openai")
        elif "(anthropic)" in selected:
            model_name = selected.split(" (")[0]
            self.ai_service.set_model(model_name, provider="anthropic")
        else:
            model_name = selected.split(" (")[0]
            self.ai_service.set_model(model_name, provider="ollama")

        self.status_var.set(f"Modèle IA sélectionné : {model_name}")

    def process_with_ai(self, action_type):
        """Traiter la note actuelle avec l'IA."""
        if not self.note_model.current_note_id:
            messagebox.showinfo("Information", "Aucune note sélectionnée")
            return

        # Récupérer le contenu
        content = self.text_area.get(1.0, tk.END).strip()

        if not content:
            messagebox.showinfo("Information", "La note est vide")
            return

        # Mise à jour du statut
        self.status_var.set(f"Traitement avec {self.ai_service.get_model()}...")
        self.root.update_idletasks()

        # Définir la fonction de callback
        def ai_callback(result):
            if result["success"]:
                if result["action"] == "correction":
                    self.text_area.delete(1.0, tk.END)
                    self.text_area.insert(tk.END, result["result"])
                    self.auto_save()
                    self.status_var.set("Correction appliquée")
                elif result["action"] == "resume":
                    ResultWindow(self.root, "Résumé", result["result"], self.theme)
                    self.status_var.set("Résumé généré")
                elif result["action"] == "categorie":
                    self.note_model.update_category(self.note_model.current_note_id, result["result"])
                    self.update_info_labels()
                    self.refresh_note_list()
                    messagebox.showinfo("Catégorisation", f"Catégorie attribuée: {result['result']}")
                    self.status_var.set("Catégorie mise à jour")
            else:
                messagebox.showerror("Erreur", result["error"])
                self.status_var.set("Erreur lors du traitement")

        # Lancer le traitement
        self.ai_service.process_with_ai(content, action_type, ai_callback)
    def open_api_key_dialog(self):
        """Fenêtre pour saisir et enregistrer une clé API."""
        def save_key():
            provider = provider_var.get()
            key = key_entry.get().strip()
            if key:
                self.ai_service.set_api_key(provider, key)
                dialog.destroy()
                messagebox.showinfo("Succès", f"Clé API pour {provider} enregistrée.")
            else:
                messagebox.showwarning("Attention", "La clé API est vide.")

        dialog = tk.Toplevel(self.root)
        dialog.title("Configurer une clé API")
        dialog.geometry("400x200")
        dialog.configure(bg=self.theme["bg"])
        dialog.transient(self.root)
        dialog.grab_set()

        tk.Label(dialog, text="Fournisseur:", bg=self.theme["bg"], fg=self.theme["fg"]).pack(pady=10)
        provider_var = tk.StringVar(value="openai")
        provider_dropdown = ttk.Combobox(dialog, textvariable=provider_var, values=["openai", "anthropic"])
        provider_dropdown.pack()

        tk.Label(dialog, text="Clé API:", bg=self.theme["bg"], fg=self.theme["fg"]).pack(pady=10)
        key_entry = tk.Entry(dialog, show="*", width=50)
        key_entry.pack(pady=5)

        save_button = tk.Button(dialog, text="Enregistrer", bg=self.theme["accent"], fg="white", command=save_key)
        save_button.pack(pady=15)

    def open_prompt_editor(self):

        prompt_file = os.path.join(os.path.expanduser("~"), "NotesAI", "prompts.json")

        default_prompts = {
            "correction": "Corrige les erreurs de grammaire, d'orthographe et de syntaxe dans ce texte, sans changer le sens et ajoute la version original du texte en bas de page: {content}",
            "resume": "Résume ce texte en conservant les points essentiels, ajoute la version originale en bas de page: {content}",
            "categorie": "Analyse ce texte et attribue-lui une catégorie parmi les suivantes : 'Travail', 'Personnel', 'Idée', 'Projet', 'Santé', 'Finance', 'Histoire', 'Informatique'. Affiche uniquement le mot de la catégorie : {content}"
        }

        if os.path.exists(prompt_file):
            with open(prompt_file, "r", encoding="utf-8") as f:
                prompts = json.load(f)
        else:
            prompts = default_prompts.copy()

        editor = tk.Toplevel(self.root)
        editor.title("Modifier les Prompts IA")
        editor.geometry("600x450")
        editor.configure(bg=self.theme["bg"])
        editor.transient(self.root)
        editor.grab_set()

        fields = {}

        for i, key in enumerate(["correction", "resume", "categorie"]):
            label = tk.Label(editor, text=f"{key.capitalize()} :", bg=self.theme["bg"], fg=self.theme["fg"])
            label.pack(anchor="w", pady=(10 if i == 0 else 5, 0), padx=10)
            entry = scrolledtext.ScrolledText(editor, height=4, wrap=tk.WORD,
                                            bg=self.theme["text_bg"], fg=self.theme["text_fg"])
            entry.pack(fill=tk.BOTH, expand=False, padx=10)
            entry.insert(tk.END, prompts.get(key, default_prompts[key]))
            fields[key] = entry

        def save_prompts():
            if not editor.winfo_exists():
                return  # Si la fenêtre a été fermée
            try:
                new_prompts = {key: fields[key].get("1.0", tk.END).strip() for key in fields}
                with open(prompt_file, "w", encoding="utf-8") as f:
                    json.dump(new_prompts, f, ensure_ascii=False, indent=2)
                editor.destroy()
                messagebox.showinfo("Succès", "Prompts sauvegardés.")
            except Exception as e:
                messagebox.showerror("Erreur", f"Erreur lors de l'enregistrement : {e}")

        def reset_to_defaults():
            if not editor.winfo_exists():
                return
            try:
                for key in fields:
                    fields[key].delete("1.0", tk.END)
                    fields[key].insert(tk.END, default_prompts[key])
            except Exception as e:
                messagebox.showerror("Erreur", f"Erreur lors de la réinitialisation : {e}")

        button_frame = tk.Frame(editor, bg=self.theme["bg"])
        button_frame.pack(pady=15)

        save_btn = tk.Button(button_frame, text="💾 Enregistrer", bg=self.theme["accent"], fg="white",
                            command=save_prompts)
        save_btn.pack(side=tk.LEFT, padx=10)

        reset_btn = tk.Button(button_frame, text="↩️ Réinitialiser", bg=self.theme["button_bg"], fg=self.theme["button_fg"],
                            command=reset_to_defaults)
        reset_btn.pack(side=tk.LEFT, padx=10)
