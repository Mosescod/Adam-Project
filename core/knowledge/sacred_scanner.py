import requests
import spacy
from collections import defaultdict
from tqdm import tqdm
import json
from pathlib import Path
from datetime import datetime

class SacredScanner:
    def __init__(self):
        self.nlp = spacy.load("en_core_web_lg")
        self.api_url = "https://api.alquran.cloud/v1"
        self.thematic_index = defaultdict(list)
        self.index_file = Path("quran_thematic_index.json")
        self.load_index()

    def load_index(self):
        if self.index_file.exists():
            with open(self.index_file, 'r') as f:
                self.thematic_index = json.load(f)

    def save_index(self):
        with open(self.index_file, 'w') as f:
            json.dump(self.thematic_index, f, indent=2)

    def scan_entire_quran(self):
        """Full Quran scan with progress tracking"""
        print("Building thematic index...")
        for surah in tqdm(range(1, 115)):  # All surahs
            data = requests.get(f"{self.api_url}/surah/{surah}/en.sahih").json()
            for ayah in data['data']['ayahs']:
                self.analyze_verse(ayah['surah']['number'], ayah['numberInSurah'], ayah['text'])
        self.save_index()

    def analyze_verse(self, surah: int, ayah: int, text: str):
        doc = self.nlp(text)
        
        # Rule-based patterns
        themes = set()
        if any(token.text.lower() in ['prophet', 'messenger'] for token in doc):
            themes.add("prophets")
        
        # Semantic similarity
        mercy_terms = ["mercy", "forgive", "compassion"]
        if any(token.similarity(self.nlp(term)) > 0.85 for term in mercy_terms for token in doc):
            themes.add("mercy")
            
        # Entity recognition
        for ent in doc.ents:
            if ent.label_ == "PERSON" and ent.text.lower() in ['solomon', 'abraham']:
                themes.add("prophets")
        
        # Store findings
        ref = f"{surah}:{ayah}"
        for theme in themes:
            self.thematic_index[theme].append({
                "ref": ref,
                "text": text,
                "keywords": [token.text for token in doc if token.is_alpha]
            })

    def get_theme_verses(self, theme: str, limit: int = 5) -> list:
        return self.thematic_index.get(theme, [])[:limit]