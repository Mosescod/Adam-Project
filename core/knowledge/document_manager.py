from typing import Dict, List
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
import logging

logger = logging.getLogger(__name__)

class DocumentManager:
    def __init__(self, scanner=None):
        self.scanner = scanner
        self.embeddings = {}
        
    def build_knowledge_base(self):
        if not self.scanner.thematic_index:
            self.scanner.scan_entire_quran()
        self._generate_embeddings()
        
    def _generate_embeddings(self):
        """Generate English-only embeddings"""
        all_texts = []
        for theme, verses in self.scanner.thematic_index.items():
            all_texts.extend(v['text'] for v in verses)
        
        if not all_texts:
            logger.warning("No texts available for embedding generation")
            return
            
        try:
            # Generate vectors per theme
            for theme, verses in self.scanner.thematic_index.items():
                texts = [v['text'] for v in verses]
                self.embeddings[theme] = self.scanner.vectorizer.transform(texts)
            logger.info(f"Generated embeddings for {len(self.embeddings)} themes")
        except Exception as e:
            logger.error(f"Error generating embeddings: {str(e)}")

    def semantic_search(self, query: str, theme: str) -> List[Dict]:
        if not hasattr(self.scanner, 'vectorizer') or not self.scanner.vectorizer:
            logger.error("Vectorizer not initialized")
            return []
            
        if theme not in self.embeddings:
            logger.warning(f"Theme '{theme}' not found in embeddings")
            return []
            
        try:
            query_vec = self.scanner.vectorizer.transform([query])
            theme_vecs = self.embeddings[theme]
            
            sims = cosine_similarity(query_vec, theme_vecs)[0]
            top_indices = np.argsort(sims)[-3:][::-1]
            return [self.scanner.thematic_index[theme][i] for i in top_indices]
        except Exception as e:
            logger.error(f"Error in semantic search: {str(e)}")
            return []