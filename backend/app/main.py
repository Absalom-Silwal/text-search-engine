import csv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from app.api.routes import search, feedback
from app.db.mongo import db
from collections import defaultdict
from app.services.search_service import SearchService
from app.helpers.search import  tokenize,clean_words,inverted_index



@asynccontextmanager
async def lifespan(app: FastAPI):
    # Ensure indexes
    await db.invert_indexes.create_index("word")
    
    # Seed data if DB is empty
    count = await db.documents.count_documents({})
    if count == 0:
        print("Seeding documents...")
        #read from csv file
        try:
            with open("app/assets/data.csv", newline="", encoding="utf-8") as f:
                reader = csv.DictReader(f)
                data = list(reader)
            if data:
                await db.documents.insert_many(data)
                
                #calculate the index
                docs = await db.documents.find({}).to_list(length=None)
                doc_tokens = defaultdict(dict)
                for doc in docs:
                    tokens = tokenize(doc['content'])
                    cleaned = clean_words(tokens)
                    doc_tokens[doc['_id']]=cleaned
                
                indexed_tokens = inverted_index(doc_tokens)
                if indexed_tokens:
                    await db.invert_indexes.insert_many(indexed_tokens)
                    
        except FileNotFoundError:
            print("data.csv not found, skipping seeding.")
    yield


app = FastAPI(title="Feedback Search Engine", lifespan=lifespan)
data = []



app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(search.router, tags=["search"])
app.include_router(feedback.router, tags=["feedback"])

if __name__ == "__main__":
    import uvicorn
    # Use reload=True only if running locally on development machine
    # Note: reload=True requires the "app.main:app" string format
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
