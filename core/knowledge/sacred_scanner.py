from logging.handlers import RotatingFileHandler
import os
import numpy as np
from typing import List, Dict, Optional
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
from .knowledge_db import KnowledgeRetriever, KnowledgeSource
import logging
from tenacity import retry, stop_after_attempt, wait_exponential
from collections import defaultdict
from sklearn.cluster import KMeans

def configure_logging():
    """Configure dual logging - file and console"""
    os.makedirs('logs', exist_ok=True)
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)
    
    file_handler = RotatingFileHandler(
        'logs/adam_system.log',
        maxBytes=5*1024*1024,
        backupCount=3
    )
    file_handler.setFormatter(logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    ))
    
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.ERROR)
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)
    
    ready_logger = logging.getLogger('adam_ready')
    ready_logger.propagate = False
    ready_handler = logging.StreamHandler()
    ready_handler.setLevel(logging.INFO)
    ready_logger.addHandler(ready_handler)

    logging.getLogger('sentence_transformers').setLevel(logging.WARNING)
    logging.getLogger('transformers').setLevel(logging.WARNING)

configure_logging()

class SacredScanner:
    def __init__(self, knowledge_db: KnowledgeRetriever):
        self.db = knowledge_db
        self.embedder = SentenceTransformer('all-MiniLM-L6-v2')
        self.theme_hierarchy = {
            'mercy': ['forgive', 'compassion', 'kindness', 'pardon', 'merciful'],
            'comfort': ['lonely', 'sad', 'ease', 'distress', 'anxiety', 'peace'],
            'prophets': ['muhammad', 'isa', 'musa', 'abraham', 'david', 'solomon'],
            'prayer': ['supplication', 'dua', 'worship', 'invocation'],
            'patience': ['perseverance', 'steadfast', 'endurance', 'trials']
        }
        self.thematic_index = defaultdict(list)
        self._refresh_thematic_index()

    @retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=4, max=10))
    def scan(self, question: str, context: Optional[Dict] = None) -> Dict[str, List[Dict]]:
        """Enhanced context-aware knowledge retrieval"""
        try:
            # Step 1: Generate embedding
            question_embedding = self.embedder.encode(question)
            logging.info(f"Generated embedding for question: {question}")
    
            # Step 2: Try vector search first
            vector_results = []
            try:
                vector_results = self.db.similarity_search_by_embedding(question_embedding, limit=25)
                logging.info(f"Found {len(vector_results)} vector results")
            
                # If we have results, process them
                if vector_results:
                    processed_results = self._process_results(vector_results)
                    return processed_results
                
            except Exception as e:
                logging.error(f"Vector search failed: {str(e)}")
    
            # Step 3: Fallback to text search if vector search fails or returns no results
            logging.info("Falling back to text search")
            text_results = self.db.text_search(question, limit=30)
            return self._process_results(text_results)
    
        except Exception as e:
            logging.error(f"Scan failed completely for question '{question}': {str(e)}", exc_info=True)
            return self._empty_response()
        
    def _process_results(self, results: List[Dict]) -> Dict[str, List[Dict]]:
        """Process raw results into organized structure"""
        if not results:
            return self._empty_response()
    
        # Ensure each result has required fields
        processed = []
        for r in results:
            if not isinstance(r, dict):
                continue
            processed.append({
                'id': r.get('_id', str(hash(str(r)))),
                'content': r.get('content', ''),
                'source': r.get('source', ''),
                'tags': r.get('tags', []),
                'metadata': r.get('metadata', {}),
                'score': r.get('score', 0.0),
                'embedding': r.get('embedding', [])
            })
    
        # Simple organization without clustering
        return {
            'verses': [r for r in processed if r.get('source') == 'quran'][:5],
            'wisdom': [r for r in processed if r.get('source') != 'quran'][:3],
            'related': [],
            'all_results': processed,
            'query_embedding': processed[0].get('embedding') if processed else None
        }
        
    def _expand_query(self, question: str, context: Dict) -> str:
        """Expand query using conversation context"""
        base_query = question
        
        if context:
            if context.get('related_themes'):
                themes = " ".join(context['related_themes'])
                base_query += f" {themes}"
            
            if context.get('mood'):
                mood = context['mood']
                if mood < 0.3:
                    base_query += " comfort guidance"
                elif mood > 0.7:
                    base_query += " joyful wisdom"
        
        return base_query

    def _cluster_by_theme(self, results: List[Dict]) -> Dict[str, List[Dict]]:
        """Organize results by thematic relevance using clustering"""
        if not results:
            return self._empty_response()
    
        # If we have fewer than 5 results, just return them directly
        if len(results) < 5:
            return {
                'verses': [r for r in results if r.get('source') == KnowledgeSource.QURAN.value][:5],
                'wisdom': [r for r in results if r.get('source') != KnowledgeSource.QURAN.value][:3],
                'related': [],
                'all_results': results,
                'query_embedding': results[0].get('embedding') if results else None
            }
        
        # Extract embeddings for clustering
        embeddings = np.array([r['embedding'] for r in results if 'embedding' in r])
        
        if len(embeddings) > 5:
            # Perform K-means clustering
            n_clusters = min(5, len(embeddings))
            kmeans = KMeans(n_clusters=n_clusters, random_state=42)
            clusters = kmeans.fit_predict(embeddings)
            
            # Group results by cluster
            clustered = defaultdict(list)
            for idx, result in enumerate(results):
                if 'embedding' in result:
                    cluster_id = clusters[idx]
                    clustered[f"cluster_{cluster_id}"].append(result)
            
            # Get top results from each cluster
            verses = []
            wisdom = []
            related = []
            
            for cluster in clustered.values():
                quran = [r for r in cluster if r.get('source') == KnowledgeSource.QURAN.value]
                others = [r for r in cluster if r.get('source') != KnowledgeSource.QURAN.value]
                
                if quran:
                    verses.extend(sorted(quran, key=lambda x: x.get('score', 0), reverse=True)[:2])
                if others:
                    wisdom.extend(sorted(others, key=lambda x: x.get('score', 0), reverse=True)[:1])
            
            # Add thematic relatedness
            if verses:
                primary_verse = verses[0]
                related = self._get_related_results(primary_verse['content'], verses)
            
            return {
                'verses': verses[:5],
                'wisdom': wisdom[:3],
                'related': related[:5],
                'all_results': results,
                'query_embedding': embeddings[0].tolist() if len(embeddings) > 0 else None
            }
        else:
            return self._empty_response()

    def _get_related_results(self, text: str, context_results: List[Dict]) -> List[Dict]:
        """Find thematically related content"""
        keywords = self._extract_keywords(text)
        themes = set()
        
        for word in keywords:
            for theme, theme_words in self.theme_hierarchy.items():
                if word in theme_words:
                    themes.add(theme)
        
        related = []
        for theme in themes:
            related.extend(self.thematic_index.get(theme, []))
        
        # Filter out already used context results
        context_ids = {r['id'] for r in context_results if 'id' in r}
        return [r for r in related if r.get('id') not in context_ids][:5]

    def _extract_keywords(self, text: str) -> List[str]:
        """Extract important keywords from text"""
        if not text:
            return []
        return [word.lower() for word in text.split() if len(word) > 3 and word.isalpha()]

    def _deduplicate_results(self, results: List[Dict]) -> List[Dict]:
        """Remove duplicate results while preserving the highest score version"""
        unique_results = {}
        for result in results:
            result_id = result.get('id')
            if result_id not in unique_results or result['score'] > unique_results[result_id]['score']:
                unique_results[result_id] = result
        return list(unique_results.values())

    def _refresh_thematic_index(self):
        """Build comprehensive thematic index"""
        self.thematic_index = defaultdict(list)
        
        for theme in self.theme_hierarchy.keys():
            try:
                quran_results = self.db.vector_search(theme, limit=20, source=KnowledgeSource.QURAN.value)
                bible_results = self.db.vector_search(theme, limit=10, source=KnowledgeSource.BIBLE.value)
                book_results = self.db.vector_search(theme, limit=5, source=KnowledgeSource.BOOK.value)
                
                self.thematic_index[theme] = quran_results + bible_results + book_results
                logging.info(f"Indexed {len(self.thematic_index[theme])} items for theme {theme}")
            except Exception as e:
                logging.error(f"Error indexing theme {theme}: {str(e)}", exc_info=True)

    def _empty_response(self) -> Dict[str, List[Dict]]:
        return {
            'verses': [],
            'wisdom': [],
            'related': [],
            'all_results': [],
            'query_embedding': None
        }