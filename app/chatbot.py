import re
from typing import Tuple, Dict


class RuleBasedChatbot:
    def __init__(self):
        self.rules = {
            "bonjour": "Bonjour ! Comment puis-je vous aider ?",
            "merci": "Avec plaisir !",
            "au revoir": "Au revoir ! Passez une excellente journee.",
            "aide": "Je peux vous aider avec : meteo, traduction, IRIS.",
        }
        self.regex_rules = {
            r"\b(meteo|temps|temperature)\b":
                "Je peux vous donner la meteo ! Dites-moi la ville.",
            r"\b(traduire|traduction|translate)\b":
                "Je peux traduire vos textes !",
        }

    def get_response(self, message: str) -> Tuple[str, str]:
        message_lower = message.lower()

        for keyword, response in self.rules.items():
            if keyword in message_lower:
                return response, "rule-based"

        for pattern, response in self.regex_rules.items():
            if re.search(pattern, message_lower):
                return response, "regex-based"

        return "Je n'ai pas bien compris. Pouvez-vous reformuler ?", "unknown"