from core.knowledge.sacred_scanner import SacredScanner
from typing import Dict, List
import numpy as np

class DocumentManager:
    def __init__(self):
        self.scanner = SacredScanner()
        self.embeddings = {}  # For semantic search
        
    def build_knowledge_base(self):
        """Periodic full scan and analysis"""
        if not self.scanner.thematic_index:
            self.scanner.scan_entire_quran()
        self._generate_embeddings()
        
    def _generate_embeddings(self):
        """Create semantic embeddings for verses"""
        for theme, verses in self.scanner.thematic_index.items():
            self.embeddings[theme] = [
                self.scanner.nlp(v['text']).vector 
                for v in verses
            ]

    def semantic_search(self, query: str, theme: str) -> List[Dict]:
        """Find most relevant verses using NLP"""
        query_vec = self.scanner.nlp(query).vector
        if theme not in self.embeddings:
            return []
            
        # Calculate cosine similarities
        sims = [
            np.dot(query_vec, verse_vec) / (np.linalg.norm(query_vec) * np.linalg.norm(verse_vec))
            for verse_vec in self.embeddings[theme]
        ]
        
        # Return top 3 most relevant verses
        top_indices = np.argsort(sims)[-3:][::-1]
        return [self.scanner.thematic_index[theme][i] for i in top_indices]