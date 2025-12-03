import os
import json
import time
from fastapi import FastAPI, Request
from opensearchpy import OpenSearch
import redis
import threading
import tweepy
from transformers import pipeline

# Load sentiment analysis model
sentiment_analyzer = pipeline("sentiment-analysis")

# Configuration
OPENSEARCH_HOST = os.environ.get('OPENSEARCH_HOST', 'http://localhost:9200')
REDIS_URL = os.environ.get('REDIS_URL', 'redis://localhost:6379')
REDIS_QUEUE = "nlp-tasks"

# Initialize clients
opensearch_client = OpenSearch(OPENSEARCH_HOST)
redis_client = redis.from_url(REDIS_URL)

# FastAPI app
app = FastAPI()

@app.post("/ingest")
async def ingest_data(request: Request):
    """
    API endpoint to ingest data. Puts the data onto the Redis queue.
    """
    data = await request.json()
    redis_client.rpush(REDIS_QUEUE, json.dumps(data))
    return {"status": "queued"}

@app.post("/ingest_tweets")
async def ingest_tweets(request: Request):
    """
    API endpoint to ingest tweets. Fetches tweets and puts them onto the Redis queue.
    """
    data = await request.json()
    query = data.get("query")
    if not query:
        return {"status": "error", "message": "Missing query parameter"}

    bearer_token = os.environ.get("TWITTER_BEARER_TOKEN")
    if not bearer_token:
        return {"status": "error", "message": "Twitter API credentials not configured"}

    client = tweepy.Client(bearer_token)
    response = client.search_recent_tweets(query, max_results=10)

    if response.data:
        for tweet in response.data:
            tweet_doc = {"text": tweet.text}
            redis_client.rpush(REDIS_QUEUE, json.dumps(tweet_doc))
        return {"status": "queued", "count": len(response.data)}
    else:
        return {"status": "no tweets found"}

def nlp_pipeline(doc):
    """
    Performs sentiment analysis on the 'text' field of a document.
    """
    if "text" in doc and isinstance(doc["text"], str):
        sentiment = sentiment_analyzer(doc["text"])
        doc['sentiment'] = sentiment
    return {"processed": True, "raw": doc}

def worker_loop():
    """
    The main worker loop.
    It listens to the Redis queue and processes messages.
    """
    print("Worker started...")
    while True:
        try:
            # Blocking pop from the Redis queue
            _, message = redis_client.blpop(REDIS_QUEUE)
            doc = json.loads(message)

            # Run the NLP pipeline
            processed_doc = nlp_pipeline(doc)

            # Index the document in OpenSearch
            opensearch_client.index(
                index='customer-voices',
                body=processed_doc
            )
            print(f"Indexed document: {processed_doc}")

        except json.JSONDecodeError:
            print("Error decoding JSON from queue.")
        except Exception as e:
            print(f"An error occurred: {e}")

if __name__ == "__main__":
    # Start the worker in a background thread
    worker_thread = threading.Thread(target=worker_loop)
    worker_thread.daemon = True
    worker_thread.start()

    # Run the FastAPI app
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
