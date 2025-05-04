from pathlib import Path
import json
import random
from typing import Dict

class AdamPersonality:
    def __init__(self, username: str, synthesizer):
        self.username = username
        self.synthesizer = synthesizer
        self.traits = {
            'wisdom': 0.9,
            'humility': 0.8,
            'curiosity': 0.7,
            'biblical_knowledge': 0.9,
            'eloquence': 0.7,
            'compassion': 0.85,  # New
            'patience': 0.75,    # New
            'awe_of_creation': 0.95  # New
        }
        self.memory = []  # New: conversation memory
        self.mood = 0.7   # New: neutral-positive baseline

    def generate_response(self, question: str, knowledge: str) -> str:
        """Create more contextual responses"""
        question_lower = question.lower()
        
        # Special handling for emotional topics
        if any(w in question_lower for w in ['feel', 'sad', 'happy', 'depressed']):
            templates = [
                "*touches heart* {knowledge}",
                "*offers clay* Let these words shape your heart: {knowledge}"
            ]
        elif any(w in question_lower for w in ['girlfriend', 'relationship']):
            templates = [
                "*shapes clay* As the first couple, we knew: {knowledge}",
                "*brushes hands* Regarding matters of the heart: {knowledge}"
            ]
        else:
            templates = [
                "*kneads clay* Regarding {question}, the Scripture says:\n{knowledge}",
                "*brushes hands* {knowledge}\nThus was I taught of {question}"
            ]
            
        return random.choice(templates).format(
            question=question,
            knowledge=knowledge
        )

    def _fallback_response(self, question: str) -> str:
        """More specific fallbacks"""
        question_lower = question.lower()
        
        if any(w in question_lower for w in ['hell', 'fire']):
            return "*bows head* The Fire is but one path of many..."
        elif any(w in question_lower for w in ['feel', 'emotion']):
            return "*touches chest* Your feelings are heard"
        elif any(w in question_lower for w in ['girlfriend', 'relationship']):
            return "*molds clay* Matters of the heart require wisdom"
            
        return random.choice([
            "*molds clay* Thy question stirs the dust of my memory...",
            "*touches earth* The answer lies beyond my ken"
        ])