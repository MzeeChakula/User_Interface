"""
Simple embeddings without sentence-transformers dependency.
Uses a basic TF-IDF approach for document similarity.
"""
from sklearn.feature_extraction.text import TfidfVectorizer
import numpy as np
from typing import List


class SimpleEmbeddings:
    """Simple TF-IDF based embeddings that don't require sentence-transformers"""
    
    def __init__(self, model_name: str = "simple-tfidf"):
        self.model_name = model_name
        self._vectorizer = None
        self._all_texts = []  # Store all texts for refitting
        
    def _get_vectorizer(self, n_docs: int):
        """Create a vectorizer appropriate for the number of documents"""
        return TfidfVectorizer(
            max_features=384,
            ngram_range=(1, 2),
            min_df=1,  # Accept terms that appear in at least 1 document
            max_df=1.0,  # Accept terms that appear in all documents
            norm='l2'
        )
        
    def embed_documents(self, texts: List[str]) -> List[List[float]]:
        """Embed a list of documents"""
        if not texts:
            return []
            
        # Add new texts to our collection
        self._all_texts.extend(texts)
        
        # Create new vectorizer and fit on all texts
        self._vectorizer = self._get_vectorizer(len(self._all_texts))
        self._vectorizer.fit(self._all_texts)
        
        # Transform only the new texts
        embeddings = self._vectorizer.transform(texts).toarray()
        return embeddings.tolist()
    
    def embed_query(self, text: str) -> List[float]:
        """Embed a single query"""
        if self._vectorizer is None:
            # If not fitted yet, create a simple vectorizer just for this query
            self._vectorizer = self._get_vectorizer(1)
            self._vectorizer.fit([text])
            
        embedding = self._vectorizer.transform([text]).toarray()[0]
        return embedding.tolist()
