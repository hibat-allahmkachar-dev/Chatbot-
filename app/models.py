from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime


class Message(BaseModel):
    """Message envoyé par l'utilisateur"""
    text: str = Field(..., min_length=1, max_length=1000,
                       example="Bonjour, comment ca va ?")


class MessageResponse(BaseModel):
    """Réponse renvoyée par le chatbot"""
    response: str
    intent: str
    service: Optional[str] = None
    timestamp: datetime


class Intent(BaseModel):
    name: str = Field(..., example="greeting")
    patterns: List[str] = Field(..., example=["bonjour", "salut"])
    responses: List[str] = Field(..., example=["Bonjour !"])


class DashboardStats(BaseModel):
    total_conversations: int
    intents_distribution: dict
    services_usage: dict
    avg_response_time: float
    uptime: float