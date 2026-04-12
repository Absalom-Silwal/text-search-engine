# Searchly Backend – Feedback-Driven Search Engine API

This repository contains the **backend service** for Searchly, a hybrid search engine that improves ranking using **TF-IDF, user feedback, and probabilistic scoring**.

---

## Features

* **TF-IDF Search Engine**

  * Inverted index-based retrieval
  * Efficient query processing

* **Feedback System**

  * Tracks user clicks per query-document pair
  * Stored in Redis for real-time updates

* **Hybrid Ranking**
  Combines:

  * TF-IDF score 
  * Click count 
  * Probability score 

  ```text
  final_score = tfidf + α * clicks + β * probability
  ```

* **Explainable Results**

  * Returns score breakdown for each result

* **CSV Data Ingestion**

  * Imports sample data from CSV
  * Stores in MongoDB before indexing

---

## Performance Optimizations

To ensure efficient and scalable search performance, the backend includes several key optimizations:


* **Batch Data Fetching**

  * Replaced sequential database and Redis calls with:

    * MongoDB batch queries
    * Redis pipeline operations
  * Significantly reduces network overhead

* **Pagination at Service Level**

  * Implements pagination using MongoDB `$in` queries
  * Fetches only required documents per page

* **Efficient Database Access**

  * Added index on:

    ```
    inverted_indexes.word
    ```
  * Speeds up term lookup during search

* **Optimized API Design**

  * Search endpoint supports:

    ```
    page, limit
    ```
  * Enables scalable result navigation

* **Faster Startup**

  * Database seeding runs only when collections are empty
  * Prevents redundant data loading

---

## Architecture


CSV -> MongoDB -> Preprocessing -> Inverted Index
                                     

Query -> SearchService -> RankingService -> Redis (Feedback)-> Final Ranking
          


---

## Tech Stack

* Python
* FastAPI
* MongoDB (document storage)
* Redis (feedback storage)
* Docker

---

## Core Services

### SearchService

* Processes query
* Computes TF-IDF scores
* Retrieves matching documents

### RankingService

* Applies hybrid scoring:

  * TF-IDF
  * Feedback boost
  * Probability score

### FeedbackService

* Stores click counts in Redis
* Key format:

  ```
  <query>:<doc_id>
  ```

---

## Setup & Run

### Docker (Recommended)

```
docker-compose up --build
```

---

### Local Setup

```
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
python -m app.main
```

---

## API Endpoints

* `POST /search` → Search documents
* `POST /feedback` → Record user click

Docs:

```
http://localhost:8080/docs
```

---

## Live API

*https://app-searchly-latest.onrender.com*

---

## Related Repository

Frontend:
*https://github.com/Absalom-Silwal/text-search-engine-frontend.git*

---

## Key Design Decisions

* **TF-IDF for rank score**

  * Simple and interpretable

* **Redis for feedback**

  * Fast real-time updates

* **MongoDB for documents**

  * Flexible schema

* **Hybrid ranking**

  * Combines tfidf + click count + probability score

---

## Future Improvements

* Upgrade to BM25
* Add semantic search
* Learning-to-rank models
* Query caching

---

