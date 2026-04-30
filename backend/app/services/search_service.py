from bson import ObjectId
from collections import defaultdict
from app.services.ranking_service import RankingService
from app.db.mongo import db
from app.db.redis import redis_client
from app.helpers.search import  tokenize,clean_words,inverted_index

class SearchService:
    async def search(query, skip=0, limit=10):
        query_tokens = tokenize(query)
        query_cleaned = clean_words(query_tokens)
        
        # RankingService now returns all relevant doc_ids with scores
        scores = await RankingService.ranking(query_cleaned)
        #print('scores',scores)
        
        total = len(scores)
        
        # Paginate the scores list first
        paginated_scores = scores[skip:skip+limit]
        
        if not paginated_scores:
            return [], total

        # Map scores for easy lookup
        score_map = {doc_id: score for doc_id, score in paginated_scores}
        doc_ids = [ObjectId(doc_id) for doc_id, _ in paginated_scores]
        
        # Fetch all document details in ONE MongoDB call
        cursor = db.documents.find({'_id': {'$in': doc_ids}})
        docs = await cursor.to_list(length=None)
        
        # Create a dictionary for mapping docs back to their scores (order from MongoDB is not guaranteed)
        doc_dict = {str(doc['_id']): doc for doc in docs}
        
        ranked_result = []
        for doc_id, score in paginated_scores:
            doc = doc_dict.get(doc_id)
            if not doc:
                continue
            
            ranked_result.append({
                "id": str(doc["_id"]),
                "title": doc["title"],
                "snippet": doc["content"][:150] + ("..." if len(doc["content"]) > 150 else ""),
                "score": score['final'],
                "tfid":score['tfid'],
                "feedback":score['feedback'],
                "explanation": f"Matched terms with calculated score {score['final']:.4f}",
                "link": doc.get("link", "")
            })

        return ranked_result, total
    
