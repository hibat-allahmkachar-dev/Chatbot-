import json


class IntentEngine:
    def __init__(self, intents_file="data/intents.json"):
        self.intents = []
        self.intent_map = {}
        self.load_intents(intents_file)

    def load_intents(self, filename):
        try:
            with open(filename, "r", encoding="utf-8") as f:
                data = json.load(f)
                self.intents = data.get("intents", [])
                for intent in self.intents:
                    self.intent_map[intent["name"]] = intent
        except FileNotFoundError:
            print(f"Fichier {filename} non trouve.")
            self.intents = []

    def get_intent(self, text: str) -> str:
        text_lower = text.lower()
        for intent in self.intents:
            for pattern in intent["patterns"]:
                if pattern in text_lower:
                    return intent["name"]
        return "unknown"

    def get_response(self, intent_name: str) -> str:
        intent = self.intent_map.get(intent_name)
        if intent and intent.get("responses"):
            return intent["responses"][0]
        return "Je n'ai pas compris. Pouvez-vous reformuler ?"