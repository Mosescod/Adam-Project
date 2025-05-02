import requests
import json
from pathlib import Path
from typing import Optional, Dict
from datetime import datetime, timedelta

class QuranAPI:
    def __init__(self):
        self.base_url = "https://api.alquran.cloud/v1"
        self.cache_file = Path("quran_cache.json")
        self.cache = self._load_cache()
        
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
    
    def search_ayah(self, keyword: str) -> Optional[str]:
        """Get verse with caching and better formatting"""
        # Check cache first
        cache_key = keyword.lower()
        if cache_entry := self.cache.get(cache_key):
            if datetime.now() < datetime.fromisoformat(cache_entry['expires']):
                return cache_entry['verse']
        
        try:
            response = requests.get(
                f"{self.base_url}/search/{keyword}/all/en.sahih",
                timeout=5  # 5-second timeout
            )
            response.raise_for_status()
            
            if matches := response.json().get('data', {}).get('matches', []):
                verse = self._format_verse(matches[0])
                
                # Cache for 7 days
                self.cache[cache_key] = {
                    'verse': verse,
                    'expires': (datetime.now() + timedelta(days=7)).isoformat()
                }
                self._save_cache()
                
                return verse
                
        except requests.exceptions.RequestException as e:
            print(f"API Error: {str(e)}")
            return None
    
    def _format_verse(self, verse_data: Dict) -> str:
        """Convert to biblical-style verse with Islamic meaning"""
        surah = verse_data['surah']['englishName']
        number = verse_data['numberInSurah']
        text = verse_data['text']
    
        # Term replacements
        replacements = {
            "Allah": "the Lord",
            "Allah's": "the Lord's",
            "your Lord": "thy God",
            "We": "I",  # Divine plural to singular
            "Quran": "Scripture"
        }
    
        for term, replacement in replacements.items():
            text = text.replace(term, replacement)
    
        return (
            f"\n📖 {surah} {number}:\n"
            f"\"{text}\"\n"
            f"—— The Holy Scripture ——"
        )