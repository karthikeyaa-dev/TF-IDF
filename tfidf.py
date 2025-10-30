from math import log, sqrt
from collections import Counter
from tqdm import tqdm
import re
import nltk
# Download NLTK stopwords if not already available
nltk.download('stopwords', quiet=True)
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer


# ---------------------- Initialization ----------------------

stop_words = set(stopwords.words('english'))
stemmer = PorterStemmer()


# ---------------------- Text Processing ----------------------


def tokenize(text, ngram_range=(1, 3)):
    """
    Tokenizes text into n-grams (e.g., unigrams, bigrams, trigrams),
    with stemming and stopword removal.
    
    Args:
        text (str): Input text.
        ngram_range (tuple): The range of n-grams to include (min_n, max_n).
                            Example: (1, 3) → unigrams, bigrams, trigrams.
    
    Returns:
        list[str]: List of tokens including n-grams.
    """
    # Basic preprocessing and tokenization
    tokens = re.findall(r'\b\w+\b', text.lower())
    tokens = [stemmer.stem(t) for t in tokens if t not in stop_words and len(t) > 1]

    # Generate n-grams
    all_ngrams = tokens.copy()
    min_n, max_n = ngram_range
    for n in range(2, max_n + 1):
        ngrams = ['_'.join(tokens[i:i+n]) for i in range(len(tokens) - n + 1)]
        all_ngrams.extend(ngrams)

    return all_ngrams



# ---------------------- Vocabulary & Frequency ----------------------

def build_vocab(corpus):
    """
    Build a sorted vocabulary from a list of documents.
    """
    vocab = set()
    for text in corpus:
        vocab.update(tokenize(text))
    return sorted(vocab)


def term_frequency(tokens, vocab):
    """
    Compute term frequency (TF) for a single document.
    Returns a list of normalized frequencies for each term in vocab.
    """
    total_counts = Counter(tokens)
    total_terms = len(tokens)
    if total_terms == 0:
        return [0] * len(vocab)

    return [total_counts.get(term, 0) / total_terms for term in vocab]


def inverse_document_frequency(corpus, vocab):
    """
    Compute inverse document frequency (IDF) across the corpus.
    """
    N = len(corpus)
    idf = []
    for term in vocab:
        df = sum(1 for text in corpus if term in tokenize(text))
        idf.append(log(N / (df + 1)) + 1)  # add 1 to avoid division by zero
    return idf


# ---------------------- Normalization ----------------------

def normalize_vector(vector):
    """
    Apply L2 normalization to a vector.
    """
    norm = sqrt(sum(x ** 2 for x in vector))
    if norm == 0:
        return vector
    return [x / norm for x in vector]


# ---------------------- TF-IDF Computation ----------------------

def compute_tfidf(corpus, vocab, idf, normalize=True):
    """
    Compute TF-IDF vectors for all documents in the corpus.
    """
    tfidf_vectors = []
    print("\n[+] Computing TF-IDF vectors...")

    for text in tqdm(corpus, desc="Processing texts", ncols=100):
        tokens = tokenize(text)
        tf = term_frequency(tokens, vocab)
        tfidf = [tf[i] * idf[i] for i in range(len(vocab))]
        if normalize:
            tfidf = normalize_vector(tfidf)
        tfidf_vectors.append(tfidf)

    print("[✓] TF-IDF computation completed.")
    return tfidf_vectors


# ---------------------- Utility ----------------------

def print_tfidf_vectors(tfidf_vectors, vocab, top_k=10):
    """
    Print top K highest TF-IDF scores per document for readability.
    """
    for i, vec in enumerate(tfidf_vectors):
        print(f"\nDocument {i+1} Top {top_k} Terms:")
        term_scores = list(zip(vocab, vec))
        top_terms = sorted(term_scores, key=lambda x: x[1], reverse=True)[:top_k]
        for term, score in top_terms:
            print(f"  {term:15s}: {score:.4f}")


corpus = [
    "the cat sat on the mat",
    "the dog sat on the log",
    "dogs and cats are great"
]

'''vocab = build_vocab(corpus)
idf = inverse_document_frequency(corpus, vocab)
tfidf_vectors = compute_tfidf(corpus, vocab, idf)
print_tfidf_vectors(tfidf_vectors,vocab)
for i, vec in enumerate(tfidf_vectors):
    print(f"Document {i+1} TF-IDF: {vec}")'''
