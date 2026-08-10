from collections import defaultdict
from datetime import datetime
import json


class ChatAnalytics:
    def __init__(self, storage_file="data/conversations.json"):
        self.storage_file = storage_file
        self.conversations = []
        self.load_conversations()

    def load_conversations(self):
        try:
            with open(self.storage_file, "r", encoding="utf-8") as f:
                self.conversations = json.load(f)
        except FileNotFoundError:
            self.conversations = []

    def log_conversation(self, message, response, intent, service=None):
        entry = {
            "timestamp": datetime.now().isoformat(),
            "message": message, "response": response,
            "intent": intent, "service": service
        }
        self.conversations.append(entry)
        with open(self.storage_file, "w", encoding="utf-8") as f:
            json.dump(self.conversations, f, ensure_ascii=False, indent=2)

    def get_stats(self) -> dict:
        total = len(self.conversations)
        if total == 0:
            return {"total_conversations": 0, "intents_distribution": {}}

        intents_count = defaultdict(int)
        for conv in self.conversations:
            intents_count[conv["intent"]] += 1

        top_intents = sorted(intents_count.items(), key=lambda x: x[1],
                              reverse=True)[:5]

        return {
            "total_conversations": total,
            "intents_distribution": dict(intents_count),
            "top_intents": top_intents
        }