from app.db.redis import redis_client
from collections import defaultdict
from app.db.mongo import db

class RankingService:
    async def ranking(query_tokens):
        scores =defaultdict(float)
        alpha = 0.3   # feedback weight
        beta = 0.5    # probability weight
        docs = await db.documents.find({}).to_list(length=None)
        for word in query_tokens:
            posting =await db.invert_indexes.find_one({'word':word})
            if not posting:
                continue
            #posting = indexed_tokens[word]
            df = len(posting)
            import math
            idf = math.log(len(docs)/df)
            for doc_id,tf in posting.get('docs').items():
                #summing all tf*idf of doc_id
                scores[doc_id] += tf * idf
            query = ' '.join(query_tokens)

            #getting total clicks of the query on all the documents
            total_query_clicks = await redis_client.get(query)
            if total_query_clicks is None:
                total_query_clicks = 0
            else:
                total_query_clicks = int(total_query_clicks)

            for doc_id,score in scores.items():
                query_key = f"{query}:{doc_id}"

                # getting click scores only on that document of that query
                click_score = await redis_client.get(query_key)
                if click_score is None:
                    click_score = 0
                else:
                    click_score = int(click_score)

                if total_query_clicks > 0:
                    click_probability = click_score / total_query_clicks
                else:
                    click_probability = 0
                scores[doc_id] = scores[doc_id] + alpha * click_score + beta * click_probability

        ranked = sorted(scores.items(), key=lambda x: x[1], reverse=True)
        return ranked
