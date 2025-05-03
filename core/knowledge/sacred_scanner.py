import requests
from collections import defaultdict
from tqdm import tqdm
import json
from pathlib import Path
from sklearn.feature_extraction.text import TfidfVectorizer
from nltk.corpus import stopwords
from nltk import pos_tag
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
import string
import re
import logging

# Initialize logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Download NLTK data
import nltk
nltk.download('punkt')
nltk.download('wordnet')
nltk.download('averaged_perceptron_tagger')
nltk.download('stopwords')

class SacredScanner:
    def __init__(self):
        self.api_url = "https://api.alquran.cloud/v1"
        self.thematic_index = defaultdict(list)
        self.index_file = Path("thematic_index.json")
        self.vectorizer = TfidfVectorizer(
            min_df=2,
            max_df=0.8,
            stop_words=stopwords.words('english'),
            token_pattern=r'\b[a-zA-Z]+\b'
        )
        self.lemmatizer = WordNetLemmatizer()
        self._all_texts = []
        self.load_index()

    def _preprocess_text(self, text: str) -> str:
        """English-specific text cleaning"""
        text = text.lower()
        text = text.translate(str.maketrans('', '', string.punctuation))
        text = re.sub(r'[^a-zA-Z\s]', '', text)
        text = ' '.join(text.split())
        return text if len(text) > 3 else ""

    def load_index(self):
        try:
            if self.index_file.exists():
                with open(self.index_file, 'r', encoding='utf-8') as f:
                    self.thematic_index = defaultdict(list, json.load(f))
                logger.info(f"Loaded index with {len(self.thematic_index)} themes")
        except Exception as e:
            logger.error(f"Error loading index: {str(e)}")

    def save_index(self):
        try:
            with open(self.index_file, 'w', encoding='utf-8') as f:
                json.dump(dict(self.thematic_index), f, indent=2)
            logger.info(f"Saved index with {len(self.thematic_index)} themes")
        except Exception as e:
            logger.error(f"Error saving index: {str(e)}")

    def scan_entire_quran(self):
        logger.info("Building thematic index...")
        for surah_num in tqdm(range(1, 115), desc="Processing Surahs"):
            try:
                response = requests.get(
                    f"{self.api_url}/surah/{surah_num}/en.sahih",
                    timeout=10
                )
                response.raise_for_status()
                data = response.json()
                
                if 'data' not in data or 'ayahs' not in data['data']:
                    logger.warning(f"Skipping surah {surah_num} - invalid structure")
                    continue
                    
                for ayah in data['data']['ayahs']:
                    clean_text = self._preprocess_text(ayah.get('text', ''))
                    if clean_text:
                        self._all_texts.append(clean_text)
                        self.analyze_verse(
                            surah_num,
                            ayah.get('numberInSurah', 0),
                            clean_text
                        )
                        
            except requests.exceptions.RequestException as e:
                logger.error(f"Network error processing surah {surah_num}: {str(e)}")
            except Exception as e:
                logger.error(f"Error processing surah {surah_num}: {str(e)}")
        
        try:
            if self._all_texts:
                self.vectorizer.fit(self._all_texts)
                logger.info("TF-IDF vectorizer fitted successfully")
        except ValueError as e:
            logger.error(f"Vectorizer error: {str(e)}")
        
        self.save_index()

    def analyze_verse(self, surah: int, ayah: int, text: str):
        tokens = word_tokenize(text)
        pos_tags = pos_tag(tokens)
        themes = set()
        
        # Rule-based theme detection
        if any(word in ['prophet', 'messenger'] for word in tokens):
            themes.add("prophets")
        
        # Similarity-based themes
        mercy_terms = ["mercy", "forgive", "compassion"]
        if any(term in text for term in mercy_terms):
            themes.add("mercy")
            
        # Store findings
        if themes:
            ref = f"{surah}:{ayah}"
            for theme in themes:
                self.thematic_index[theme].append({
                    "ref": ref,
                    "text": text,
                    "keywords": [word for word in tokens 
                               if word not in stopwords.words('english')]
                })

    def get_theme_verses(self, theme: str, limit: int = 5) -> list:
        return self.thematic_index.get(theme, [])[:limit]