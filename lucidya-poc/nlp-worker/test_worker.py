import unittest
from unittest.mock import patch, MagicMock
from worker import nlp_pipeline, app
from fastapi.testclient import TestClient

class TestNLPPipeline(unittest.TestCase):

    def setUp(self):
        self.client = TestClient(app)

    def test_sentiment_analysis(self):
        """
        Tests that the NLP pipeline correctly adds sentiment to a document.
        """
        doc = {"text": "I love this product!"}
        processed_doc = nlp_pipeline(doc)
        self.assertIn("sentiment", processed_doc["raw"])
        self.assertIsInstance(processed_doc["raw"]["sentiment"], list)
        self.assertIn("label", processed_doc["raw"]["sentiment"][0])

    @patch('os.environ.get')
    @patch('worker.tweepy.Client')
    @patch('worker.redis_client')
    def test_ingest_tweets(self, mock_redis_client, mock_tweepy_client, mock_os_get):
        """
        Tests the /ingest_tweets endpoint.
        """
        # Mock the environment variable
        mock_os_get.return_value = "dummy_token"
        # Mock the Twitter API response
        mock_tweet = MagicMock()
        mock_tweet.text = "This is a test tweet."
        mock_tweepy_client.return_value.search_recent_tweets.return_value = MagicMock(data=[mock_tweet])

        # Make the request to the endpoint
        response = self.client.post("/ingest_tweets", json={"query": "test"})

        # Assert that the response is correct
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"status": "queued", "count": 1})

        # Assert that the tweet was added to the Redis queue
        mock_redis_client.rpush.assert_called_once_with("nlp-tasks", '{"text": "This is a test tweet."}')

if __name__ == '__main__':
    unittest.main()
