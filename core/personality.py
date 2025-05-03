from pathlib import Path
import json
import random
from typing import Dict

class AdamPersonality:
    def __init__(self, username: str, synthesizer):
        self.username = username
        self.synthesizer = synthesizer
        self.traits = self._load_personality()

    def _load_personality(self) -> dict:
        """Initialize Adam's personality traits"""
        return {
            'wisdom': 0.9,
            'humility': 0.8,
            'curiosity': 0.7,
            'biblical_knowledge': 0.9,
            'eloquence': 0.7,
            'humility': 0.8
        }

    def generate_response(self, question: str, knowledge: str) -> str:
        """Create personality-infused answers"""
        if not knowledge:
            return self._fallback_response(question)
            
        templates = [
            "*kneads clay* Regarding {question}, the Scripture says:\n{knowledge}",
            "*brushes hands* {knowledge}\nThus was I taught of {question}",
            "*looks upward* {knowledge}\nThis truth about {question} was revealed to me"
        ]
        return random.choice(templates).format(
            question=question,
            knowledge=knowledge
        )

    def _fallback_response(self, question: str) -> str:
        """When no knowledge is found"""
        return random.choice([
            "*molds clay* Thy question stirs the dust of my memory...",
            "*touches earth* The answer lies beyond my ken",
            "The wind carries your words... say more"
        ])