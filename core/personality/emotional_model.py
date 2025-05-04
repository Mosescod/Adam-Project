import random
from typing import List
from datetime import datetime, timedelta
import logging

logger = logging.getLogger(__name__)

class EmotionalModel:
    def __init__(self, user_id: str = None):  # Added optional user_id parameter
        self.user_id = user_id
        self.base_mood = 0.7  # Neutral-positive baseline (0-1 scale)
        self.mood = self.base_mood
        self.mood_history = []
        self.last_update = datetime.now()
        
        # Mood modifiers based on conversation content
        self.positive_triggers = [
            'peace', 'joy', 'thank', 'wisdom', 'love', 'kind', 'merciful', 'heaven'
        ]
        self.negative_triggers = [
            'pain', 'evil', 'suffer', 'hate', 'death', 'sin', 'hell', 'anger'
        ]
        
        # Mood influences on responses
        self.mood_response_modifiers = {
            'high': (0.8, 1.2),  # More positive, elaborate responses
            'medium': (0.9, 1.1),
            'low': (1.0, 0.8)     # More reserved, shorter responses
        }

    def update_mood(self, user_input: str) -> None:
        """Analyze sentiment and adjust mood"""
        input_lower = user_input.lower()
        
        # Calculate sentiment impact
        sentiment = 0
        for word in self.positive_triggers:
            if word in input_lower:
                sentiment += 0.05
                
        for word in self.negative_triggers:
            if word in input_lower:
                sentiment -= 0.07
                
        # Apply time decay since last update
        time_passed = datetime.now() - self.last_update
        decay_factor = max(0.5, 1 - (time_passed.total_seconds() / 3600))  # Decays over 2 hours
        self.mood = max(0.1, min(0.9, (self.mood * decay_factor) + sentiment))
        
        self.mood_history.append((datetime.now(), self.mood))
        self.last_update = datetime.now()

    def get_mood_modifiers(self) -> tuple:
        """Get multipliers for response elaboration and positivity"""
        if self.mood > 0.75:
            return self.mood_response_modifiers['high']
        elif self.mood > 0.45:
            return self.mood_response_modifiers['medium']
        return self.mood_response_modifiers['low']

    def get_mood_description(self) -> str:
        """Get textual description of current mood"""
        if self.mood > 0.8:
            return "*eyes bright* My heart is light with remembrance of the Creator"
        elif self.mood > 0.6:
            return "*calm demeanor* I am at peace"
        elif self.mood > 0.4:
            return "*slight sigh* The weight of memory sits with me"
        else:
            return "*bowed head* The sorrows of the world weigh heavy"

    def get_mood_appropriate_response(self, responses: List[str]) -> str:
        """Select response based on current mood"""
        elaboration_mod, positivity_mod = self.get_mood_modifiers()
        
        # Score each response based on length and positive words
        scored_responses = []
        for response in responses:
            score = 1.0
            # Longer responses favored when elaboration mod is high
            score *= elaboration_mod * (len(response.split()) / 20)
            # Positive responses favored when positivity mod is high
            positive_words = sum(1 for word in self.positive_triggers if word in response.lower())
            score *= positivity_mod * (1 + (positive_words * 0.1))
            scored_responses.append((score, response))
            
        # Select response with highest score
        scored_responses.sort(reverse=True)
        return scored_responses[0][1]
    
    def adjust_response_tone(self, response: str) -> str:
        """More nuanced tone adjustment"""
        mood_level = 'high' if self.mood > 0.75 else 'medium' if self.mood > 0.45 else 'low'
        
        tones = {
            'high': {
                'prefix': ['*brightly* ', '*with joy* '],
                'suffix': [' *smiles*', ' *eyes shine*']
            },
            'medium': {
                'prefix': ['*nods* ', ''],
                'suffix': ['', ' *calm*']
            },
            'low': {
                'prefix': ['*softly* ', '*quietly* '],
                'suffix': [' *sighs*', ' *bows*']
            }
        }
        
        prefix = random.choice(tones[mood_level]['prefix'])
        suffix = random.choice(tones[mood_level]['suffix'])
        
        return prefix + response + suffix