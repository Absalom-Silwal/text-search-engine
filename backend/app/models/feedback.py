from pydantic import BaseModel
from datetime import datetime

class Feedback(BaseModel):
    query: str
    doc_id: str
    timestamp: datetime = datetime.now()
