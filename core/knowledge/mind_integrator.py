from .quran_db import QuranDatabase
from datetime import datetime, timedelta
import logging
from typing import Optional
from typing import Dict

logger = logging.getLogger(__name__)

class DivineKnowledge:
    def __init__(self, quran_db):
        self.db = quran_db
        self.term_map = {
            "Allah": "the Lord",
            "Paradise": "the Garden",
            "Messenger": "Prophet",
            "We": "I",
            "verily": "truly"
        }
        
        self.priority_verses = {
            "creation": "15:26-29",
            "afterlife": "2:25",
            "forgiveness": "39:53",
            "adam": "2:30-33",
            "eve": "4:1",
            "lonely": "94:5-6",
            "patience": "2:153",
            "hell": "3:131",
            "depression": "94:5",
            "comfort": "2:286",
            "relationships": "30:21"
        }

    def search_verse(self, query: str, context: list = None) -> str:  # Add context parameter
        """Search with optional conversation context"""
        if context:
            # Boost relevance of verses mentioned in recent context
            context_keywords = " ".join([q["question"] for q in context[-2:]])
            query = f"{query} {context_keywords}"  # Augment search query
        
        # Emotional support cases
        if 'feel bad' in query or 'depressed' in query:
            return self._format_verse(self.db.get_verse_by_reference("94:5"))
        if 'lonely' in query:
            return self._format_verse(self.db.get_verse_by_reference("93:3"))
        if 'relationship' in query or 'girlfriend' in query:
            return self._format_verse(self.db.get_verse_by_reference("30:21"))
        
        # Check priority verses first
        for term, ref in self.priority_verses.items():
            if term in query:
                verse = self._get_verse_by_ref(ref)
                if verse:
                    return self._format_verse(verse)
        
        # Then try thematic search using scanner's themes
        themes_to_try = [
            'creation', 'mercy', 'prophets', 
            'afterlife', 'forgiveness'
        ]
        
        for theme in themes_to_try:
            if theme in query:
                verses = self.db.get_verses_by_theme(theme, limit=1)
                if verses:
                    return self._format_verse(verses[0])
        
        # Fallback to general search
        verses = self.db.search_verses(query, limit=1)
        return self._format_verse(verses[0]) if verses else None

    # ... rest of the class remains the same ...

    def _get_verse_by_ref(self, ref: str) -> Optional[Dict]:
        """Get verse by reference, handling ranges"""
        if '-' in ref:
            base_ref = ref.split('-')[0]
            verse = self.db.get_verse_by_reference(base_ref)
            if verse:
                verse['text'] += "..."  # Indicate continuation
            return verse
        return self.db.get_verse_by_reference(ref)

    def _format_verse(self, verse: Dict) -> str:
        """Format verse with biblical terms"""
        if not verse:
            return ""
            
        text = verse['text']
        for term, replacement in self.term_map.items():
            text = text.replace(term, replacement)
        
        return (
            f"{verse['surah_name']} {verse['ayah_number']}:\n"
            f"\"{text}\"\n"
            f"—— The Holy Scripture ——"
        )