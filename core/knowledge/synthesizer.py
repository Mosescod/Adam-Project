from datetime import datetime
import re
from typing import List, Dict, Optional
import numpy as np
from collections import Counter
from sklearn.feature_extraction.text import TfidfVectorizer
from .knowledge_db import KnowledgeSource

class UniversalSynthesizer:
    def __init__(self, knowledge_db):
        self.db = knowledge_db
        self.vectorizer = TfidfVectorizer(stop_words='english', max_features=5000)
        
    def blend(self, scanner_output: Dict, context: Optional[Dict] = None) -> Dict:
        """Analyze all results and generate comprehensive response"""
        if not scanner_output or not scanner_output.get('all_results'):
            return self._empty_response()

        all_results = scanner_output['all_results']
        
        # Process all 15 results
        analysis = self._analyze_all_results(all_results, context)
        
        return {
            'content': self._format_prophetic_response(analysis),
            'primary_theme': analysis['primary_theme'],
            'sources': all_results[:3],
            'supporting_sources': all_results[3:6],
            'confidence': analysis['confidence'],
            'mood_score': analysis['mood_score'],
            'detected_themes': analysis['themes']
        }

    def _analyze_all_results(self, results: List[Dict], context: Optional[Dict]) -> Dict:
        """Deep analysis of all search results"""
        # 1. Extract and clean all content
        contents = [self._clean_content(r['content']) for r in results]
        
        # 2. Identify key themes
        themes = self._identify_common_themes(contents)
        
        # 3. Extract key facts
        key_facts = self._extract_key_facts(contents)
        
        # 4. Find representative quotes
        quotes = self._find_representative_quotes(results)
        
        # 5. Determine confidence
        confidence = min(0.8 + (len(results)/30), 0.95)  # More results = higher confidence
        
        return {
            'primary_theme': themes[0] if themes else 'divine wisdom',
            'themes': themes,
            'key_facts': key_facts,
            'quotes': quotes,
            'confidence': confidence,
            'mood_score': 0.7 if 'mercy' in themes else 0.5
        }

    def _format_prophetic_response(self, analysis: Dict) -> str:
        """Convert analysis into Adam's prophetic response"""
        response_parts = []
        
        # 1. Time-based opening
        hour = datetime.now().hour
        if hour < 12:
            response_parts.append("As the morning light reveals...")
        else:
            response_parts.append("As the day unfolds...")
        
        # 2. Clay action + theme introduction
        response_parts.append("*kneads clay thoughtfully* The scriptures speak of this matter...")
        
        # 3. Main themes
        if analysis['themes']:
            response_parts.append(f"The primary wisdom concerns {', '.join(analysis['themes'][:3])}.")
        
        # 4. Key facts
        if analysis['key_facts']:
            response_parts.append("*shapes words in clay* Know these truths:")
            response_parts.extend(f"- {fact}" for fact in analysis['key_facts'][:3])
        
        # 5. Representative quotes
        if analysis['quotes']:
            response_parts.append("*etches sacred words* Remember these teachings:")
            response_parts.extend(f"* '{quote}'" for quote in analysis['quotes'][:2])
        
        # 6. Prophetic conclusion
        response_parts.append("*brushes hands* Thus is wisdom preserved across the ages.")
        
        return "\n".join(response_parts)
    
    def _clean_content(self, text: str) -> str:
        """Clean and normalize text content"""
        if not text:
            return ""
        
        # Remove references like (Quran 2:255)
        text = re.sub(r'\([^)]*\)', '', text)
        # Remove verse numbers
        text = re.sub(r'\b\d+:\d+\b', '', text)
        # Remove special characters except basic punctuation
        text = re.sub(r'[^\w\s.,;!?\']', '', text)
        # Normalize whitespace
        text = ' '.join(text.split())
        return text.strip()

    def _identify_common_themes(self, texts: List[str]) -> List[str]:
        """Find common themes across all texts"""
        # Use TF-IDF to find important terms
        tfidf = TfidfVectorizer(stop_words='english', max_features=20)
        try:
            tfidf.fit(texts)
            return tfidf.get_feature_names_out().tolist()
        except:
            return ['divine wisdom', 'sacred knowledge']

    def _extract_key_facts(self, texts: List[str]) -> List[str]:
        """Extract key factual statements"""
        facts = []
        for text in texts[:10]:  # Analyze first 10 to prevent overload
            # Simple fact extraction - first sentence of each relevant result
            first_sentence = re.split(r'[.!?]', text)[0]
            if len(first_sentence) > 20:  # Minimum length
                facts.append(first_sentence.strip())
        return facts[:5]  # Return top 5 facts

    def _find_representative_quotes(self, results: List[Dict]) -> List[str]:
        """Find the most representative quotes"""
        quotes = []
        for result in results:
            if result.get('source') == 'quran':
                # For Quranic verses, use the full content
                quotes.append(self._clean_content(result['content']))
            else:
                # For others, extract notable statements
                text = result.get('content', '')
                notable = re.findall(r'\"(.*?)\"|“(.*?)”', text)
                quotes.extend([q[0] or q[1] for q in notable if any(q)])
        return quotes[:4]  # Return top 4 quotes

    def _combine_sources(self, verses: List[Dict], wisdom: List[Dict]) -> List[Dict]:
        """Combine and weight sources by importance"""
        combined = []
        
        # Add Quran verses first with highest weight
        for verse in verses:
            verse['weight'] = self.theme_weights.get('quran', 1.5)
            combined.append(verse)
        
        # Add other religious texts
        for wisdom_text in wisdom:
            source_type = wisdom_text.get('source', '').lower()
            weight = self.theme_weights.get(source_type, 1.0)
            wisdom_text['weight'] = weight
            combined.append(wisdom_text)
        
        # Sort by weight then score
        return sorted(combined, 
                     key=lambda x: (x['weight'], x.get('score', 0)), 
                     reverse=True)

    def _create_unified_content(self, sources: List[Dict]) -> str:
        """Create coherent response from multiple sources"""
        if not sources:
            return "I need more time to contemplate this question"
        
        # Start with primary source
        primary = sources[0]
        content = primary['content']
        
        # Add supporting points if available
        if len(sources) > 1:
            supporting = sources[1]
            content += f"\n\nAs mentioned in {supporting.get('source', 'another source')}:"
            content += f"\n{supporting['content'][:200]}..."
        
        return content

    def _analyze_themes(self, sources: List[Dict]) -> List[str]:
        """Identify themes across all sources"""
        texts = [s['content'] for s in sources]
        tags = []
        
        # Get tags from all sources
        for s in sources:
            tags.extend(s.get('tags', []))
        
        # Analyze text content
        if texts:
            self.vectorizer.fit(texts)
            terms = self.vectorizer.get_feature_names_out()
            scores = np.sum(self.vectorizer.transform(texts).toarray(), axis=0)
            top_terms = [terms[i] for i in np.argsort(scores)[-5:][::-1]]
            
            # Match terms to themes
            detected = []
            for term in top_terms + tags:
                for theme, keywords in self.theme_hierarchy.items():
                    if term in keywords and theme not in detected:
                        detected.append(theme)
            
            return detected
        
        return []

    def _determine_primary_theme(self, themes: List[str]) -> str:
        """Select most relevant theme"""
        if not themes:
            return 'default'
        
        # Count theme occurrences
        counts = Counter(themes)
        return counts.most_common(1)[0][0]

    def _calculate_confidence(self, sources: List[Dict]) -> float:
        """Calculate confidence based on source quality and quantity"""
        if not sources:
            return 0.0
            
        base_conf = min(0.7 + (len(sources) * 0.05), 0.95)
        weighted_conf = base_conf * sources[0]['weight']
        return min(weighted_conf, 1.0)

    def _analyze_mood(self, sources: List[Dict]) -> float:
        """Analyze emotional tone across sources (0=sad, 1=joyful)"""
        positive = ['hope', 'love', 'peace', 'joy', 'mercy']
        negative = ['lonely', 'suffering', 'pain', 'fear', 'anger']
        
        score = 0.5
        for s in sources:
            text = s['content'].lower()
            score += sum(0.02 for word in positive if word in text)
            score -= sum(0.02 for word in negative if word in text)
        
        return np.clip(score, 0.1, 0.9)

    def _empty_response(self) -> Dict:
        """Return empty response structure"""
        return {
            'content': "I need more time to contemplate this question",
            'primary_theme': 'default',
            'sources': [],
            'supporting_sources': [],
            'confidence': 0.0,
            'mood_score': 0.5,
            'detected_themes': [],
            'contextual_embedding': None
        }