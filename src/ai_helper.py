# file: ai_explainer.py

import json
import urllib.request
from dataclasses import dataclass
from typing import Optional
from utils.message import notify

@dataclass
class AIConfig:
    """A simple data class to hold AI configuration."""
    host: str
    api_key: str
    model: str = "gpt-3.5-turbo"

class AIHelper:
    """Handles all communication with a class-OpenAI LLM API."""

    def __init__(self, config: AIConfig):
        """
        Initializes the AIExplainer with the necessary configuration.
        
        Args:
            config: An AIConfig object containing the host, API key, and model name.
        """
        self.config = config

    def get_explanation(self, sentence: str, word: str) -> Optional[str]:
        """
        Calls the AI API to get a one-sentence explanation of a word in context.

        Args:
            sentence: The full sentence containing the word.
            word: The word to be explained.

        Returns:
            The AI-generated explanation as a string, or None if it fails.
        """
        prompt = f"请解释单词 “{word}” 在 “{sentence}” 这个句子中的意思和用法。"
        api_url = f"{self.config.host.rstrip('/')}/v1/chat/completions"
        
        payload = {
            "model": self.config.model,
            "messages": [{"role": "user", "content": prompt}],
            "temperature": 0.7,
            "max_tokens": 10000
        }
        
        request_data = json.dumps(payload).encode("utf-8")
        headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {self.config.api_key}'
        }

        try:
            print("Requesting AI explanation...")
            print(f'api_url: {api_url}  request_data: {request_data}')
            request = urllib.request.Request(api_url, data=request_data, headers=headers, method='POST')
            with urllib.request.urlopen(request) as response:
                if response.status != 200:
                    print(f"AI API Error: Received HTTP {response.status} {response.reason}")
                    return None
                
                response_body = response.read().decode("utf-8")
                response_dict = json.loads(response_body)
                explanation = response_dict['choices'][0]['message']['content'].strip()
                print(f"Successfully received AI explanation: {explanation}")
                return explanation
        except Exception as e:
            print(f"An error occurred while calling the AI API: {e}")
            notify("AI Explanation Failed", f"Error: {e}")
            return None