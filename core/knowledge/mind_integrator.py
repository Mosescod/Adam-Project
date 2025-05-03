import requests
from datetime import datetime, timedelta
from pathlib import Path
import json
from typing import Dict, Optional

class DivineKnowledge:
    def __init__(self):
        self.base_url = "https://api.alquran.cloud/v1"
        self.cache_file = Path("core/knowledge/data/mind_cache.json")
        self.cache = self._load_cache()
        
        # Biblical term replacements
        self.term_map = {
            "Allah": "the Lord",
            "Paradise": "the Garden",
            "Messenger": "Prophet",
            "We": "I"  # Divine plural to singular
        }
        
        # Priority verses for common questions
        self.priority_verses = {
            "creation": "15:26",
            "afterlife": "2:25",
            "forgiveness": "39:53",
            "adam": "2:30-33"
        }

    def _load_cache(self) -> Dict:
        """Load cached verses with expiration"""
        if self.cache_file.exists():
            with open(self.cache_file, 'r') as f:
                return json.load(f)
        return {}

    def _save_cache(self):
        """Save cache to disk"""
        with open(self.cache_file, 'w') as f:
            json.dump(self.cache, f)

    def search_verse(self, keyword: str) -> str:
        """Search with caching and biblical phrasing"""
        # Check cache first
        cache_key = keyword.lower()
        if cache_entry := self.cache.get(cache_key):
            if datetime.now() < datetime.fromisoformat(cache_entry['expires']):
                return cache_entry['verse']

        try:
            # Check priority verses
            for term, ref in self.priority_verses.items():
                if term in keyword.lower():
                    return self._get_specific_verse(ref)

            # Fallback to search
            response = requests.get(
                f"{self.base_url}/search?query={keyword}&translation=en",
                timeout=3
            )
            response.raise_for_status()
            
            if verses := response.json().get('verses', []):
                formatted = self._format_verse(verses[0])
                
                # Cache for 24 hours
                self.cache[cache_key] = {
                    'verse': formatted,
                    'expires': (datetime.now() + timedelta(hours=24)).isoformat()
                }
                self._save_cache()
                
                return formatted
                
        except Exception as e:
            print(f"API Error: {str(e)}")
        return ""

    def _get_specific_verse(self, ref: str) -> str:
        """Fetch specific verse by reference"""
        try:
            surah, verse = ref.split(':')
            response = requests.get(
                f"{self.base_url}/{surah}/{verse}?translation=en",
                timeout=3
            )
            if response.status_code == 200:
                return self._format_verse(response.json())
        except:
            pass
        return ""

    def _format_verse(self, verse: Dict) -> str:
        """Apply biblical phrasing"""
        text = verse['translation']
        for term, replacement in self.term_map.items():
            text = text.replace(term, replacement)
        
        return (
            f"{verse['surah_name']} {verse['verse_number']}:\n"
            f"\"{text}\"\n"
            f"—— The Holy Scripture ——"
        )