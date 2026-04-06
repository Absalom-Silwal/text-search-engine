from app.db.redis import redis_client
from app.models.feedback import Feedback
from app.helpers.search import tokenize,clean_words

class FeedbackService:
    @staticmethod
    async def record_click(feedback: Feedback):
        # Format query to ensure consistency
        #query = feedback.query.lower().strip()
        query_tokens = tokenize(feedback.query)
        query_cleaned = clean_words(query_tokens)
        query = ' '.join(query_cleaned)
        document_key = f"{query}:{feedback.doc_id}"
        await redis_client.incr(document_key)
        await redis_client.incr(query)
        # Set expiration to 30 days
        await redis_client.expire(document_key, 30 * 24 * 60 * 60)
        await redis_client.expire(query, 30 * 24 * 60 * 60)
