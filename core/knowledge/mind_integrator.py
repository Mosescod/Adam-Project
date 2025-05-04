from .quran_db import QuranDatabase
import logging
from typing import Optional, Dict

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

    def search_verse(self, query: str) -> str:
        """Search with priority verse handling"""
        try:
            # Check priority verses first
            for term, ref in self.priority_verses.items():
                if term in query.lower():
                    verse = self._get_verse_by_ref(ref)
                    if verse:
                        return self._format_verse(verse)
            
            # Fallback logic
            verses = self.db.search_verses(query, limit=1)
            if verses:
                return self._format_verse(verses[0])
            
            return self._format_verse(self.db.get_verse_by_reference("2:21"))
            
        except Exception as e:
            logger.error(f"Verse search failed: {str(e)}")
            return "*brushes hands* The answer eludes me today"

    def _get_verse_by_ref(self, ref: str) -> Optional[Dict]:
        """Get verse by reference with error handling"""
        try:
            return self.db.get_verse_by_reference(ref)
        except Exception as e:
            logger.error(f"Failed to get verse {ref}: {str(e)}")
            return None

    def _format_verse(self, verse: Dict) -> str:
        """Format verse with both reference styles"""
        if not verse:
            return ""
            
        text = verse['text']
        for term, replacement in self.term_map.items():
            text = text.replace(term, replacement)
        
        return (
            f"{verse['surah_name']} {verse['ayah_number']} (Surah {verse['surah_number']}:{verse['ayah_number']}):\n"
            f"\"{text}\"\n"
            f"—— The Holy Scripture ——"
        )