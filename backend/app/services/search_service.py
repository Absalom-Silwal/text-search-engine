from typing import List, Dict
from bson import ObjectId
from collections import defaultdict
#from app.search.bm25 import BM25Search
from app.services.ranking_service import RankingService
from app.db.mongo import db
from app.db.redis import redis_client
from app.helpers.search import  tokenize,clean_words,inverted_index

class SearchService:
    async def search(query):
        docs = await db.documents.find({}).to_list(length=None)
        doc_tokens = defaultdict(dict)
        for doc in docs:
            print('doc',doc)
            tokens = tokenize(doc['content'])
            cleaned = clean_words(tokens)
            doc_tokens[doc['_id']]=cleaned
        #inverted indexing
        indexed_tokens = inverted_index(doc_tokens)
        query_tokens = tokenize(query)
        query_cleaned = clean_words(query_tokens)
        scores = await RankingService.ranking(docs,query_cleaned,indexed_tokens)
        print('scores',scores)
        ranked_result = []
        for score in scores:
            doc = await db.documents.find_one({'_id': ObjectId(score[0])})
            ranked_result.append({
                "id": str(doc["_id"]),
                "title": doc["title"],
                "snippet": doc["content"][:150] + "...",
                "score":score[1],
                "explanation": f"Matched terms with TF‑IDF score {score[1]:.4f}"
            })

        return ranked_result
    
