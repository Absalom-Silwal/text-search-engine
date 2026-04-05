from app.db.redis import redis_client
from app.models.feedback import Feedback

class FeedbackService:
    @staticmethod
    async def record_click(feedback: Feedback):
        # Format query to ensure consistency
        query = feedback.query.lower().strip()
        key = f"clicks:{query}:{feedback.doc_id}"
        await redis_client.incr(key)
        # Set expiration to 30 days
        await redis_client.expire(key, 30 * 24 * 60 * 60)
