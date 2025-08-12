# file: your_anki_file.py (replace your original code with this)

import json
import urllib.request
from typing import Any, Dict, Optional

# from base import Application
from utils.message import notify
from ai_helper import AIHelper, AIConfig

class AnkiNoteUpdater:
    """
    Manages updating Anki notes, with optional AI-powered field population.
    This class handles all Anki-Connect communication and orchestration logic.
    """
    
    def __init__(self, config, app, args, ai_explainer: Optional[AIHelper] = None):
        """
        Initializes the updater.

        Args:
            config: The main application configuration object (e.g., from configparser).
            ai_explainer: An optional instance of AIHelper. If provided, AI features are enabled.
        """
        self.config = config
        self.app = app
        self.args = args
        if not ai_explainer:
            if config.getboolean('Anki', 'enable-AI-explanation', fallback=False) or self.args.extra == 'AI':
                ai_conf = AIConfig(
                    host=config.get('Anki', 'AI-host'),
                    api_key=config.get('Anki', 'AI-key'),
                    model=config.get('Anki', 'AI-model') 
                )
                ai_explainer = AIHelper(ai_conf)
        self.ai_explainer = ai_explainer # Dependency Injection
        self.anki_url = self.config.get('Anki', 'url')
        self.deck_name = self.config.get('Anki', 'deck')

    def _invoke_anki_connect(self, action: str, **params: Any) -> Dict[str, Any]:
        """A private helper to make generic calls to the Anki-Connect API."""
        payload = json.dumps({"action": action, "params": params, "version": 6}).encode("utf-8")
        request = urllib.request.Request(self.anki_url, data=payload, headers={'Content-Type': 'application/json'})
        
        with urllib.request.urlopen(request) as response:
            response_body = response.read().decode("utf-8")
            response_dict = json.loads(response_body)
            if response_dict.get("error") is not None:
                raise ConnectionError(f"Anki API Error: {response_dict['error']}")
            return response_dict.get("result")

    def process_app_request(self):
        """
        The main entry point to process an app request and update the latest Anki note.
        This orchestrates the entire workflow.
        """
        try:
            print("Starting Anki note update process...")
            
            # 1. Find the latest note
            note_ids = self._invoke_anki_connect("findNotes", query=f"deck:{self.deck_name}")
            if not note_ids:
                raise ValueError(f"No notes found in deck '{self.deck_name}'.")
            latest_note_id = max(note_ids)
            print(f"Found latest note with ID: {latest_note_id}")

            # 2. Get existing note data
            note_info = self._invoke_anki_connect("notesInfo", notes=[latest_note_id])[0]
            current_fields = {name: data['value'] for name, data in note_info['fields'].items()}
            
            # 3. Prepare new data and merge it
            fields_from_app = {'Text': self.app.text, 'Link': self.app.origin_link}
            current_fields.update(fields_from_app)

            # 4. (Optional) Get AI explanation
            updated_field_keys = list(fields_from_app.keys())
            if self.ai_explainer:
                word = note_info['fields'].get('Front', {}).get('value')
                sentence = current_fields.get('Text')
                
                if word and sentence:
                    ai_insight = self.ai_explainer.get_explanation(sentence=sentence, word=word)
                    if ai_insight:
                        # Add explanation to the 'aiInsight' field.
                        # IMPORTANT: Ensure your Anki note type has a field named 'aiInsight'.
                        current_fields['AI-Insight'] = ai_insight
                        updated_field_keys.append('AI-Insight')
                else:
                    print("Warning: Missing 'Front' or 'Text' field. Cannot generate AI explanation.")

            # 5. Update the note in Anki
            payload = {"note": {"id": latest_note_id, "fields": current_fields}}
            self._invoke_anki_connect("updateNoteFields", **payload)
            
            print(f"Successfully updated note {latest_note_id} with fields: {updated_field_keys}")
            notify("Anki Update Successful", f"Updated fields for the latest note.")

        except Exception as e:
            print(f"An error occurred during the note update process: {e}")
            notify("Anki Update Failed", f"Error: {e}")