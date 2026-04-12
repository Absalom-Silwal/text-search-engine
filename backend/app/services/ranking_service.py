from app.db.redis import redis_client
from collections import defaultdict
from app.db.mongo import db

class RankingService:
    async def ranking(query_tokens):
        scores = defaultdict(float)
        alpha = 0.3   # feedback weight
        beta = 0.5    # probability weight
        
        # 1. Get total number of documents (N)
        N = await db.documents.count_documents({})
        if N == 0:
            return []

        # 2. Fetch all postings for all query tokens in one go
        cursor = db.invert_indexes.find({'word': {'$in': query_tokens}})
        postings = await cursor.to_list(length=None)
        
        import math
        
        # 3. Calculate TF-IDF component
        for posting in postings:
            # df is the number of documents containing this word
            docs_map = posting.get('docs', {})
            df = len(docs_map)
            if df == 0:
                continue
            
            idf = math.log(N / df)
            for doc_id, tf in docs_map.items():
                scores[doc_id] += tf * idf
        
        if not scores:
            return []

        query = ' '.join(query_tokens)

        # 4. Handle click-based ranking outside the word loop
        total_query_clicks = await redis_client.get(query)
        total_query_clicks = int(total_query_clicks) if total_query_clicks else 0

        # 5. Use Redis Pipeline to fetch all click scores in one roundtrip
        async with redis_client.pipeline(transaction=False) as pipe:
            doc_ids = list(scores.keys())
            for doc_id in doc_ids:
                pipe.get(f"{query}:{doc_id}")
            click_scores_raw = await pipe.execute()
        
        # 6. Final score calculation
        for i, doc_id in enumerate(doc_ids):
            click_score = int(click_scores_raw[i]) if click_scores_raw[i] else 0
            
            click_probability = click_score / total_query_clicks if total_query_clicks > 0 else 0
            
            scores[doc_id] += alpha * click_score + beta * click_probability

        ranked = sorted(scores.items(), key=lambda x: x[1], reverse=True)
        return ranked
