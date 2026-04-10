import re
from nltk.stem import PorterStemmer
from collections import defaultdict

STOP_WORDS = {
    "the", "a", "an", "and", "or", "but", "if", "then", "else",
    "on", "in", "at", "to", "from", "by", "with", "of", "for",
    "is", "are", "was", "were", "be", "been", "being"
}

from collections import defaultdict

def tokenize(text: str):
    return re.findall(r'\b\w+\b', text.lower())

def remove_punctuation(word: str) -> str:
    return re.sub(r"[^\w\s]", "", word)

def clean_words(words):
    stemmer = PorterStemmer()
    cleaned = []
    for w in words:
        #Stemming / Lemmatization
        w = stemmer.stem(remove_punctuation(w.lower()))
        if w and w not in STOP_WORDS:
            cleaned.append(w)
    return cleaned

def inverted_index(docs_list):
    index = defaultdict(dict)
    for doc_id, doc in enumerate(docs_list.items()):
        # Count words in this document once
        freq = {}
        for word in (doc[1]):
            if word in freq:
                freq[word] += 1
            else:
                freq[word] = 1
        for word,count in freq.items():
            #index.append({'word':word,'docs':{'docs':1,'docs2':3}})
            index[word][str(doc[0])] = count
    return [
        {'word':word,'docs':docs} for word,docs in index.items()
    ]
            

    return index