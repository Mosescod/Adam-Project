from .mind_integrator import DivineKnowledge
from typing import Dict, Optional


class DocumentSynthesizer:
    def __init__(self, documents: Dict[str, str]):
        self.documents = documents
        self.mind = DivineKnowledge()

    def get_insights(self, question: str) -> list:
        themes = self.analyzer.detect_themes(question) 
        
    def query(self, question: str) -> Optional[str]:
        """Search documents for answers with basic NLP"""
        question = question.lower().strip('?')
        
        # Exact match
        if question in self.documents:
            return self.documents[question]
            
        # Partial match
        for key, answer in self.documents.items():
            if key in question:
                return answer
                
        return None
    
    def get_insights(self, question: str) -> Optional[str]:
        """Priority: Qur'an > Documents"""
        # 1. Check for Qur'anic queries
        islamic_keywords = ['allah', 'quran', 'prophet', 'sin', 'paradise']
        if any(kw in question.lower() for kw in islamic_keywords):
            if ayah := self.quran.search_ayah(question):
                return ayah
        
        # 2. Fallback to documents
        return self.documents.get(question.lower())