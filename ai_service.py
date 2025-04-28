"""
Module de service d'IA pour l'intégration avec différents services d'IA.
"""
import requests
from threading import Thread
import os
import json

class AIService:
    """Service d'intégration avec différents services d'IA."""

    def __init__(self):
        # Configuration par défaut
        self.providers = {
            "ollama": {
                "url": "http://localhost:11434/api/generate",
                "model": "mistral",
                "type": "local"
            },
            "openai": {
                "url": "https://api.openai.com/v1/chat/completions",
                "model": "gpt-3.5-turbo",
                "type": "cloud"
            },
            "anthropic": {
                "url": "https://api.anthropic.com/v1/messages",
                "model": "claude-3-haiku-20240307",
                "type": "cloud"
            }
        }
        
        self.current_provider = "ollama"
        self.api_keys = self.load_api_keys()

    def load_api_keys(self):
        """Charger les clés API depuis un fichier de configuration."""
        config_path = os.path.join(os.path.expanduser("~"), "NotesAI", "config.json")
        
        # Créer le dossier s'il n'existe pas
        os.makedirs(os.path.dirname(config_path), exist_ok=True)
        
        # Initialiser avec des valeurs par défaut si le fichier n'existe pas
        default_keys = {
            "openai_api_key": "",
            "anthropic_api_key": ""
        }
        
        try:
            if os.path.exists(config_path):
                with open(config_path, 'r') as f:
                    return json.load(f)
            else:
                with open(config_path, 'w') as f:
                    json.dump(default_keys, f, indent=2)
                return default_keys
        except Exception as e:
            print(f"Erreur lors du chargement des clés API : {e}")
            return default_keys

    def save_api_keys(self, api_keys):
        """Sauvegarder les clés API dans un fichier de configuration."""
        config_path = os.path.join(os.path.expanduser("~"), "NotesAI", "config.json")
        try:
            with open(config_path, 'w') as f:
                json.dump(api_keys, f, indent=2)
            return True
        except Exception as e:
            print(f"Erreur lors de la sauvegarde des clés API : {e}")
            return False

    def set_api_key(self, provider, api_key):
        """Définir une clé API pour un fournisseur."""
        provider_key = f"{provider}_api_key"
        self.api_keys[provider_key] = api_key
        self.save_api_keys(self.api_keys)

    def set_model(self, model_name, provider=None):
        """Définir le modèle et le fournisseur à utiliser."""
        if provider:
            # Vérifier si le fournisseur existe
            if provider not in self.providers:
                raise ValueError(f"Fournisseur {provider} non supporté")
            self.current_provider = provider
        
        # Mettre à jour le modèle pour le fournisseur actuel
        self.providers[self.current_provider]["model"] = model_name

    def get_model(self):
        """Obtenir le modèle actuel."""
        return self.providers[self.current_provider]["model"]

    def process_with_ai(self, content, action_type, callback):
        """
        Traiter du contenu avec l'IA.

        Args:
            content (str): Le contenu à traiter
            action_type (str): Le type d'action ('correction', 'resume', 'categorie')
            callback (function): Fonction de rappel à appeler avec le résultat
        """
        if not content:
            callback({"success": False, "error": "Le contenu est vide"})
            return

        # Lancer le traitement dans un thread séparé
        Thread(target=self._process_async, args=(content, action_type, callback)).start()

def _process_async(self, content, action_type, callback):
    """
    Traiter de manière asynchrone avec le service d'IA.

    Args:
        content (str): Le contenu à traiter
        action_type (str): Le type d'action
        callback (function): Fonction de rappel à appeler avec le résultat
    """
    try:
        provider_info = self.providers[self.current_provider]

        # Charger les prompts personnalisés
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
            prompts = default_prompts

        prompt_template = prompts.get(action_type)
        if not prompt_template:
            callback({"success": False, "error": f"Prompt introuvable pour l'action : {action_type}"})
            return

        prompt = prompt_template.replace("{content}", content)

        # Traitement selon le type de fournisseur
        if provider_info["type"] == "local":
            response = self._process_ollama(prompt, provider_info)
        elif provider_info["type"] == "cloud":
            if self.current_provider == "openai":
                response = self._process_openai(prompt, provider_info)
            elif self.current_provider == "anthropic":
                response = self._process_anthropic(prompt, provider_info)

        # Traiter le résultat
        if response.status_code == 200:
            result = self._extract_result(response, provider_info)

            if action_type == "correction":
                callback({"success": True, "action": "correction", "result": result})
            elif action_type == "resume":
                callback({"success": True, "action": "resume", "result": result})
            elif action_type == "categorie":
                category = result.split("\n")[0].strip()
                if len(category.split()) > 3:
                    category = " ".join(category.split()[:2])
                callback({"success": True, "action": "categorie", "result": category})
        else:
            error_msg = f"Erreur {self.current_provider}: {response.status_code} - {response.text}"
            callback({"success": False, "error": error_msg})

    except Exception as e:
        callback({"success": False, "error": str(e)})

    def _process_ollama(self, prompt, provider_info):
        """Traitement via Ollama local."""
        data = {
            "model": provider_info["model"],
            "prompt": prompt,
            "stream": False
        }
        return requests.post(provider_info["url"], json=data)

    def _process_openai(self, prompt, provider_info):
        """Traitement via OpenAI."""
        api_key = self.api_keys.get("openai_api_key", "")
        if not api_key:
            raise ValueError("Clé API OpenAI manquante")

        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }
        data = {
            "model": provider_info["model"],
            "messages": [{"role": "user", "content": prompt}]
        }
        return requests.post(provider_info["url"], headers=headers, json=data)

    def _process_anthropic(self, prompt, provider_info):
        """Traitement via Anthropic."""
        api_key = self.api_keys.get("anthropic_api_key", "")
        if not api_key:
            raise ValueError("Clé API Anthropic manquante")

        headers = {
            "x-api-key": api_key,
            "Content-Type": "application/json",
            "anthropic-version": "2023-06-01"
        }
        data = {
            "model": provider_info["model"],
            "max_tokens": 4096,
            "messages": [{"role": "user", "content": prompt}]
        }
        return requests.post(provider_info["url"], headers=headers, json=data)

    def _extract_result(self, response, provider_info):
        """Extraire le résultat selon le fournisseur."""
        data = response.json()
        
        if provider_info["type"] == "local":
            return data["response"].strip()
        elif self.current_provider == "openai":
            return data["choices"][0]["message"]["content"].strip()
        elif self.current_provider == "anthropic":
            return data["content"][0]["text"].strip()