from typing import List, Dict
import redis.asyncio as redis
from collections import defaultdict

class RankingService:
    async def ranking(docs,query_tokens,indexed_tokens):
        scores =defaultdict(float)
        for word in query_tokens:
            if word not in indexed_tokens:
                continue
            posting = indexed_tokens[word]
            df = len(posting)
            import math
            idf = math.log(len(docs)/df)
            for doc_id,tf in posting.items():
                #summing all tf*idf of doc_id
                scores[doc_id] += tf * idf

        ranked = sorted(scores.items(), key=lambda x: x[1], reverse=True)
        return ranked
