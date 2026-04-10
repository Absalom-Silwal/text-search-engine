from bson import ObjectId
from collections import defaultdict
from app.services.ranking_service import RankingService
from app.db.mongo import db
from app.db.redis import redis_client
from app.helpers.search import  tokenize,clean_words,inverted_index

class SearchService:
    async def search(query):
        query_tokens = tokenize(query)
        query_cleaned = clean_words(query_tokens)
        scores = await RankingService.ranking(query_cleaned)
        ranked_result = []
        for score in scores:
            doc = await db.documents.find_one({'_id': ObjectId(score[0])})
            ranked_result.append({
                "id": str(doc["_id"]),
                "title": doc["title"],
                "snippet": doc["content"][:150] + "...",
                "score":score[1],
                "explanation": f"Matched terms with TF‑IDF score {score[1]:.4f}",
                "link":doc["link"]
            })

        return ranked_result
    
