# 🔍 Feedback-Driven Search Engine

A minimal, production-structured MVP of a search engine that improves ranking based on user clicks.

## 🚀 Features
- **Keyword Search:** Uses BM25 (via `rank-bm25`) for initial document retrieval.
- **Feedback Loop:** Captures clicks on search results.
- **Dynamic Ranking:** Adjusts scores using the formula: `final_score = bm25_score + 0.3 * click_count`.
- **Modern Stack:** FastAPI, React (Vite), MongoDB, and Redis.

## 🏗️ Architecture
- **Backend (FastAPI):**
  - `SearchService`: Coordinates BM25 search and result hydration.
  - `RankingService`: Merges BM25 scores with feedback boosts from Redis.
  - `FeedbackService`: Increments click counts in Redis for specific query-document pairs.
- **Frontend (React):**
  - `SearchBar`: Trigger searches.
  - `ResultsList`: Displays results with scores and explanations.
  - `useSearch`: Custom hook managing state and feedback logic.
- **Storage:**
  - **MongoDB:** Stores document content and metadata.
  - **Redis:** Stores click counts with query-based keys (e.g., `clicks:fastapi:doc_1`).

## 🛠️ Setup & Run

### Method 1: Docker (Recommended)
```bash
docker-compose up --build
```

### Method 2: Locally Only (Manual Setup)
1. **Prerequisites:**
   - Install MongoDB and Redis.
   - Install Python 3.11+.
   - Install Node.js 20+.
2. **Setup Backend:**
   ```bash
   cd backend
   python -m venv venv
   source venv/bin/activate  # or venv\Scripts\activate
   pip install -r requirements.txt
   python -m app.main
   ```
3. **Setup Frontend:**
   ```bash
   cd frontend
   npm install
   npm run dev
   ```

- **Frontend:** [http://localhost:5173](http://localhost:5173)
- **Backend API:** [http://localhost:8000](http://localhost:8000)
- **API Docs (Swagger):** [http://localhost:8000/docs](http://localhost:8000/docs)

## 📊 How it works
1. **Initial Search:** When you search for "fastapi", the system calculates BM25 scores for all matching documents.
2. **Clicking:** If you click on a result, a POST request is sent to `/feedback`.
3. **Boosting:** The next time you search for the same term, the clicked document's score is boosted.
   - `Boost = 0.3 * clicks`
4. **Explanation:** Each result shows its score breakdown (e.g., `BM25(1.2) + FeedbackBoost(0.6)`).

## 📄 Sample Data
The system automatically seeds 10 sample documents (FastAPI, React, Redis, Docker, etc.) on the first run.
