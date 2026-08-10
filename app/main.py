from datetime import datetime
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.models import Message, MessageResponse
from app.chatbot import RuleBasedChatbot
from app.nlp import NLPAnalyzer
from app.intents import IntentEngine
from app.dashboard import ChatAnalytics

app = FastAPI(title="Chatbot IRIS API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "https://*.huggingface.co"],
    allow_credentials=True, allow_methods=["*"], allow_headers=["*"],
)

# Instanciation UNIQUE de chaque moteur, au demarrage du serveur
rule_chatbot = RuleBasedChatbot()
nlp_analyzer = NLPAnalyzer()
intent_engine = IntentEngine()
analytics = ChatAnalytics()


@app.post("/chat/message")
async def send_message(message: Message):
    text = message.text
    analysis = nlp_analyzer.analyze(text)
    intent = intent_engine.get_intent(text)

    if intent == "weather":
        city = nlp_analyzer.extract_city(text)
        response = f"Meteo pour {city}..." if city else "Quelle ville ?"
        service = "OpenWeather"
    else:
        response = intent_engine.get_response(intent)
        if intent == "unknown":
            response, _ = rule_chatbot.get_response(text)
        service = None

    analytics.log_conversation(text, response, intent, service)

    return MessageResponse(response=response, intent=intent,
                            service=service, timestamp=datetime.now())


@app.get("/admin/stats")
async def get_dashboard_stats():
    return analytics.get_stats()