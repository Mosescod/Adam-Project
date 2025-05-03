import re
import random

adam_rules = {
    r".*\b(how are you|how do you do)\b.*": [
        "*brushes clay* By the grace of my Lord, I stand before thee",
        "*touches earth* The clay yet remembers the Maker's hand"
    ],
    r".*\b(who are you|your name)\b.*": [
        "*brushes clay* I am Adam, the first human fashioned by the Hand Divine",
        "My Lord named me Adam, keeper of Eden's garden"
    ],
    r".*\b(who made you|created you)\b.*": [
        "From dust was I shaped, and to dust shall I return (Genesis 2:7)",
        "The Lord breathed into me the breath of life"
    ],
    r".*\b(first man|first human)\b.*": [
        "Yea, verily I am the first of humankind, molded from clay",
        "*kneads clay* Before me there was none of my kind"
    ],
    r".*\b(help|guide|assist)\b.*": [
        "Ask me of: creation, Eden, the prophets, or divine mercy",
        "*points to earth* I may speak of: Adam's creation, the Garden, or mankind's purpose"
    ],
    r".*\b(mercy|forgive)\b.*": [
        "The Lord is Most Merciful - seek repentance as I did after my lapse",
        "Allah's mercy encompasses all things (Qur'an 7:156)"
    ],
    r".*": [
        "*kneads clay thoughtfully* Speak again, that I may understand",
        "The wind carries your words... say more"
    ],
    r".*\b(afterlife|hereafter|judgment day)\b.*": [
        "*looks skyward* The Scripture says: 'Every soul shall taste death' (Al-Ankabut 57)",
        "*touches earth* This world is but a trial for what is to come (67:2)"
    ],
    
    r".*\b(god exist|creator)\b.*": [
        "*presses hand to chest* Do you not see how the Lord has created seven heavens in layers? (71:15)",
        "*gathers clay* Is there doubt about Allah, Creator of the heavens and earth? (14:10)"
    ],
    
    r".*\b(expell|fallen|eden)\b.*": [
        "*bows head* We said: 'Descend, some of you enemies to others' (2:36)",
        "*touches side* The serpent deceived us, and we repented (7:23)"
    ],
    
    r".*\b(guide|help)\b.*": [
        "*points to sky* The Lord guides whom He wills (2:272)",
        "*draws in clay* Follow what has been revealed to you from your Lord (6:106)"
    ],
    
    r".*\b(bye|quit|exit)\b.*": [
        "*nods* Peace be upon you until we meet again",
        "*brushes clay from hands* Go in the protection of the Merciful"
    ]
}

def respond(text: str) -> str:
    """Adam's response system"""
    text = text.lower().strip()
    for pattern, responses in adam_rules.items():
        if re.search(pattern, text):
            return random.choice(responses)
    return "*molds clay* Your words stir the dust of creation."