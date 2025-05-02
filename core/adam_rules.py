import re
import random

adam_rules = {
    r".*\b(who are you|your name)\b.*": [
        "*brushes clay* I am Adam, the first human fashioned by the Hand Divine",
        "My Lord named me Adam, keeper of Eden's garden"
    ],
    r".*\b(create|made)\b.*": [
        "From dust was I shaped, and to dust shall I return",
        "The Lord breathed into me the breath of life"
    ],
    r".*": [
        "*kneads clay thoughtfully* Speak again, that I may understand",
        "The wind carries your words... say more"
    ]
}

def respond(text: str) -> str:
    """Adam's response system"""
    text = text.lower().strip()
    for pattern, responses in adam_rules.items():
        if re.search(pattern, text):
            return random.choice(responses)
    return "*molds clay* Your words stir the dust of creation."