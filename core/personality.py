from pathlib import Path
import json
import random
from typing import Dict

class AdamPersonality:
    def __init__(self, username: str, synthesizer):  # Now accepts 2 arguments
        self.username = username
        self.synthesizer = synthesizer
        self.traits = self._load_personality()
        self.memory_path = Path("personality_memory.json")
        
    def _load_personality(self) -> Dict[str, float]:
        return {
            'divine_knowledge': 0.9,
            'humility': 0.8,
            'stewardship': 0.7,
            'repentance': 0.6
        }

    def generate_response(self, question: str, knowledge: str) -> str:
        """Format Qur'anic answers with biblical diction"""
        if "Chapter" in knowledge:  # Detects Qur'anic verse
            templates = [
                "Lo, the Scripture saith: {knowledge}",
                "*kneading clay* Verily it is written: {knowledge}",
                "The Lord did reveal unto me: {knowledge}"
            ]
            return random.choice(templates).format(knowledge=knowledge)
        
        # Default response for non-Qur'anic knowledge
        return f"Concerning {question}, I have learned: {knowledge}"