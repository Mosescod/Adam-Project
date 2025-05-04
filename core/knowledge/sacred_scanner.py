from typing import Dict, List
from .quran_db import QuranDatabase
import logging
from sklearn.feature_extraction.text import TfidfVectorizer

logger = logging.getLogger(__name__)

class SacredScanner:
    def __init__(self):
        self.db = QuranDatabase()
        self.vectorizer = TfidfVectorizer(
            min_df=2,
            max_df=0.8,
            stop_words='english',
            token_pattern=r'\b[a-zA-Z]+\b'
        )
        self.default_themes = {  # Moved here from QuranDatabase
            'creation': ['create', 'made', 'form'],
            'mercy': ['mercy', 'compassion', 'forgive'],
            'prophets': ['prophet', 'messenger', 'apostle']
        }
        self._initialize()

    def _initialize(self):
        """Initialize with default data"""
        if not self.db.is_populated():
            logger.info("Populating Quran database...")
            if not self._populate_database():
                raise Exception("Failed to initialize Quran database")

    def _populate_database(self) -> bool:
        """Load initial data into database"""
        translations = {
            'en.sahih': 'https://api.alquran.cloud/v1/quran/en.sahih'
        }
        
        if not self.db.store_entire_quran(translations):
            return False

        # Add default themes
        default_themes = {
            'creation': ['create', 'made', 'form'],
            'mercy': ['mercy', 'compassion', 'forgive'],
            'prophets': ['prophet', 'messenger', 'apostle']
        }
        
        for theme, keywords in default_themes.items():
            self.db.add_theme(theme, keywords)
            
        return True

    def scan_entire_quran(self) -> bool:
        """Main scanning method - ensures database is ready"""
        return self.db.is_populated() or self._populate_database()

    def get_theme_verses(self, theme: str, limit: int = 5) -> List[Dict]:
        """Get verses by theme"""
        return self.db.get_verses_by_theme(theme)[:limit]

    def semantic_search(self, query: str, theme: str = None) -> List[Dict]:
        """Enhanced search with optional theme filtering"""
        if theme:
            return self.db.get_verses_by_theme(theme)
        return self.db.search_verses(query)