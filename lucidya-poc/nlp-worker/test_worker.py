import unittest
from worker import nlp_pipeline

class TestNLPPipeline(unittest.TestCase):

    def test_sentiment_analysis(self):
        """
        Tests that the NLP pipeline correctly adds sentiment to a document.
        """
        doc = {"text": "I love this product!"}
        processed_doc = nlp_pipeline(doc)
        self.assertIn("sentiment", processed_doc["raw"])
        self.assertIsInstance(processed_doc["raw"]["sentiment"], list)
        self.assertIn("label", processed_doc["raw"]["sentiment"][0])

    def test_emotion_detection(self):
        """
        Tests that the NLP pipeline correctly adds emotion to a document.
        """
        doc = {"text": "I am so happy!"}
        processed_doc = nlp_pipeline(doc)
        self.assertIn("emotions", processed_doc["raw"])
        self.assertIsInstance(processed_doc["raw"]["emotions"], list)
        self.assertIn("label", processed_doc["raw"]["emotions"][0][0])

if __name__ == '__main__':
    unittest.main()
