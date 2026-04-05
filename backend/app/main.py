from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from app.api.routes import search, feedback
from app.db.mongo import db
from app.services.search_service import SearchService

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Seed data if DB is empty
    count = await db.documents.count_documents({})
    if count == 0:
        sample_docs = [
            {"title": "FastAPI Guide", "content": "FastAPI is a modern web framework for building APIs with Python."},
            {"title": "React Best Practices", "content": "React is a JavaScript library for building user interfaces."},
            {"title": "MongoDB for Beginners", "content": "MongoDB is a source-available cross-platform document-oriented database program."},
            {"title": "Redis Performance", "content": "Redis is an in-memory data structure store, used as a distributed, in-memory key–value database."},
            {"title": "Python for Data Science", "content": "Python is a high-level programming language known for its readability and versatility."},
            {"title": "Vite: Next Generation Frontend Tooling", "content": "Vite is a build tool that aims to provide a faster and leaner development experience."},
            {"title": "Machine Learning Overview", "content": "Machine learning is a field of study in artificial intelligence that gives computers the ability to learn without being explicitly programmed."},
            {"title": "Docker in Production", "content": "Docker is a set of platform as a service products that use OS-level virtualization to deliver software in packages called containers."},
            {"title": "Microservices Architecture", "content": "Microservices are an architectural style that structures an application as a collection of services."},
            {"title": "Clean Code Principles", "content": "Clean code is code that is easy to understand and easy to change."},
        ]
        await db.documents.insert_many(sample_docs)
    yield


app = FastAPI(title="Feedback Search Engine", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
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
