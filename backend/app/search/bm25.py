# from rank_bm25 import BM25Okapi
# from typing import List, Dict
# import re

# def tokenize(text: str) -> List[str]:
#     return re.findall(r'\w+', text.lower())

# class BM25Search:
#     def __init__(self, documents: List[Dict]):
#         self.doc_ids = [doc["_id"] for doc in documents]
#         self.corpus = [tokenize(doc["title"] + " " + doc["content"]) for doc in documents]
#         self.bm25 = BM25Okapi(self.corpus)

#     def search(self, query: str) -> List[Dict]:
#         tokenized_query = tokenize(query)
#         scores = self.bm25.get_scores(tokenized_query)
        
#         results = []
#         for idx, score in enumerate(scores):
#             if score > 0:
#                 results.append({
#                     "id": self.doc_ids[idx],
#                     "score": float(score)
#                 })
        
#         return sorted(results, key=lambda x: x["score"], reverse=True)
