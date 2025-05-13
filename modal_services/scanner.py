import modal
import numpy as np
from sentence_transformers import SentenceTransformer
from pymongo import MongoClient
import os
from typing import Dict, List

app = modal.App("adam-scanner")  # Changed from Stub to App
image = modal.Image.debian_slim().pip_install(
    "sentence-transformers",
    "pymongo",
    "numpy",
    "scikit-learn"
)

@app.cls(image=image, gpu="T4", min_containers=1)  # Changed keep_warm to min_containers
class SacredScanner:
    def __enter__(self):
        self.model = SentenceTransformer('all-MiniLM-L6-v2')
        self.db = MongoClient(os.getenv("MONGODB_URI"))["AdamAI-KnowledgeDB"]
        self.theme_hierarchy = {
            'mercy': ['forgive', 'compassion', 'kindness', 'pardon', 'merciful'],
            'comfort': ['lonely', 'sad', 'ease', 'distress', 'anxiety', 'peace'],
            'prophets': ['muhammad', 'isa', 'musa', 'abraham', 'david', 'solomon'],
            'prayer': ['supplication', 'dua', 'worship', 'invocation'],
            'patience': ['perseverance', 'steadfast', 'endurance', 'trials']
        }

    @modal.method()
    def scan(self, question: str, context: Dict = None) -> Dict[str, List[Dict]]:
        """Enhanced context-aware knowledge retrieval"""
        try:
            # Generate embedding
            question_embedding = self.model.encode(question)
            
            # Vector search
            vector_results = list(self.db.entries.aggregate([
                {
                    "$vectorSearch": {
                        "index": "adamai_search",
                        "path": "vector",
                        "queryVector": question_embedding.tolist(),
                        "numCandidates": 150,
                        "limit": 25
                    }
                },
                {"$project": {
                    "_id": 1,
                    "content": 1,
                    "source": 1,
                    "tags": 1,
                    "metadata": 1,
                    "score": {"$meta": "vectorSearchScore"}
                }}
            ]))
            
            if vector_results:
                return self._process_results(vector_results)
                
            # Fallback to text search
            text_results = list(self.db.entries.find(
                {"$text": {"$search": question}},
                {"score": {"$meta": "textScore"}}
            ).limit(30))
            
            return self._process_results(text_results)
            
        except Exception as e:
            return self._empty_response()

    def _process_results(self, results: List[Dict]) -> Dict[str, List[Dict]]:
        """Process raw results into organized structure"""
        if not results:
            return self._empty_response()
            
        processed = [{
            'id': str(r['_id']),
            'content': r.get('content', ''),
            'source': r.get('source', ''),
            'tags': r.get('tags', []),
            'metadata': r.get('metadata', {}),
            'score': r.get('score', 0.0),
            'embedding': r.get('vector', [])
        } for r in results]
        
        return {
            'verses': [r for r in processed if r.get('source') == 'quran'][:5],
            'wisdom': [r for r in processed if r.get('source') != 'quran'][:3],
            'all_results': processed,
            'query_embedding': processed[0].get('embedding') if processed else None
        }

    def _empty_response(self) -> Dict[str, List[Dict]]:
        return {
            'verses': [],
            'wisdom': [],
            'all_results': [],
            'query_embedding': None
        }