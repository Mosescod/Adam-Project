from .quran import QuranAPI
from typing import Dict, Optional

class DocumentSynthesizer:
    def __init__(self, documents: Dict[str, str]):
        self.documents = documents
        self.quran = QuranAPI()
        
    def get_insights(self, question: str) -> Optional[str]:
        """Priority: Qur'an > Documents"""
        # 1. Check for Qur'anic queries
        islamic_keywords = ['allah', 'quran', 'prophet', 'sin', 'paradise']
        if any(kw in question.lower() for kw in islamic_keywords):
            if ayah := self.quran.search_ayah(question):
                return ayah
        
        # 2. Fallback to documents
        return self.documents.get(question.lower())