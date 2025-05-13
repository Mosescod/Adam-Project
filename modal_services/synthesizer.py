import modal
from datetime import datetime
import re
from typing import List, Dict
from transformers import pipeline
import numpy as np
from collections import Counter
from sklearn.feature_extraction.text import TfidfVectorizer

app = modal.App("adam-synthesizer")  # Changed from Stub to App
image = modal.Image.debian_slim().pip_install(
    "transformers",
    "torch",
    "scikit-learn",
    "numpy"
)

@app.cls(image=image, gpu="A10G", min_containers=1)  # Changed keep_warm to min_containers
class UniversalSynthesizer:
    def __enter__(self):
        self.summarizer = pipeline(
            "summarization",
            model="sshleifer/distilbart-cnn-12-6"
        )
        self.theme_analyzer = pipeline(
            "text2text-generation",
            model="google-t5/t5-base"
        )
        self.vectorizer = TfidfVectorizer(stop_words='english', max_features=20)

    @modal.method()
    def blend(self, scanner_output: Dict, context: Dict = None) -> Dict:
        """Analyze results and generate comprehensive response"""
        if not scanner_output or not scanner_output.get('all_results'):
            return self._empty_response()
            
        all_results = scanner_output['all_results']
        contents = [self._clean_content(r['content']) for r in all_results]
        
        # Extract themes
        themes = self._identify_common_themes(contents)
        
        # Generate response
        response = self._format_prophetic_response({
            'themes': themes,
            'key_facts': self._extract_key_facts(contents),
            'quotes': self._find_representative_quotes(all_results),
            'confidence': min(0.8 + (len(all_results)/30), 0.95)
        })
        
        return {
            'content': response,
            'primary_theme': themes[0] if themes else 'divine wisdom',
            'confidence': 0.9,
            'mood_score': 0.7 if 'mercy' in themes else 0.5
        }

    def _clean_content(self, text: str) -> str:
        if not text:
            return ""
        text = re.sub(r'\([^)]*\)|\b\d+:\d+\b|[^\w\s.,;!?\']', '', text)
        return ' '.join(text.split()).strip()

    def _identify_common_themes(self, texts: List[str]) -> List[str]:
        try:
            self.vectorizer.fit(texts)
            return self.vectorizer.get_feature_names_out().tolist()
        except:
            return ['divine wisdom', 'sacred knowledge']

    def _extract_key_facts(self, texts: List[str]) -> List[str]:
        return [re.split(r'[.!?]', text)[0].strip() 
                for text in texts[:10] 
                if len(re.split(r'[.!?]', text)[0]) > 20][:5]

    def _find_representative_quotes(self, results: List[Dict]) -> List[str]:
        quotes = []
        for result in results:
            if result.get('source') == 'quran':
                quotes.append(self._clean_content(result['content']))
            else:
                notable = re.findall(r'\"(.*?)\"|“(.*?)”', result.get('content', ''))
                quotes.extend([q[0] or q[1] for q in notable if any(q)])
        return quotes[:4]

    def _format_prophetic_response(self, analysis: Dict) -> str:
        response = [
            "As the morning light reveals..." if datetime.now().hour < 12 
            else "As the day unfolds...",
            "*kneads clay thoughtfully* The scriptures speak of this matter..."
        ]
        
        if analysis['themes']:
            response.append(f"The primary wisdom concerns {', '.join(analysis['themes'][:3])}.")
        
        if analysis['key_facts']:
            response.append("*shapes words in clay* Know these truths:")
            response.extend(f"- {fact}" for fact in analysis['key_facts'][:3])
        
        if analysis['quotes']:
            response.append("*etches sacred words* Remember these teachings:")
            response.extend(f"* '{quote}'" for quote in analysis['quotes'][:2])
        
        response.append("*brushes hands* Thus is wisdom preserved across the ages.")
        return "\n".join(response)

    def _empty_response(self) -> Dict:
        return {
            'content': "I need more time to contemplate this question",
            'primary_theme': 'default',
            'confidence': 0.0,
            'mood_score': 0.5
        }