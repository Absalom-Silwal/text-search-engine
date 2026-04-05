from fastapi import APIRouter
from app.models.feedback import Feedback
from app.services.feedback_service import FeedbackService

router = APIRouter()

@router.post("/feedback")
async def record_feedback(feedback: Feedback):
    await FeedbackService.record_click(feedback)
    return {"status": "ok"}
