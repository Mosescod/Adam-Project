import json
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

class DocumentKnowledge:
    def __init__(self, file_path="data/documents.json"):
        with open(file_path) as f:
            self.documents = json.load(f)
        
        self.vectorizer = TfidfVectorizer()
        self._train_vectorizer()

    def _train_vectorizer(self):
        texts = [doc['text'] for doc in self.documents]
        self.vectorizer.fit(texts)

    def search(self, query):
        query_vec = self.vectorizer.transform([query])
        doc_vecs = self.vectorizer.transform([doc['text'] for doc in self.documents])
        
        similarities = cosine_similarity(query_vec, doc_vecs)[0]
        top_indices = similarities.argsort()[-3:][::-1]
        
        return {
            'documents': [self.documents[i] for i in top_indices]
        }