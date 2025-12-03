import os
from opensearchpy import OpenSearch

# Configuration
OPENSEARCH_HOST = os.environ.get('OPENSEARCH_HOST', 'http://localhost:9200')

def generate_report():
    """
    Generates a simple report of the sentiment data in OpenSearch.
    """
    client = OpenSearch(OPENSEARCH_HOST)

    # Query OpenSearch for all documents in the customer-voices index
    response = client.search(
        index="customer-voices",
        body={"query": {"match_all": {}}}
    )

    # Process the results and generate a report
    report = "Sentiment Analysis Report\n"
    report += "=========================\n\n"

    for hit in response["hits"]["hits"]:
        source = hit["_source"]["raw"]
        text = source.get("text", "N/A")
        sentiment = source.get("sentiment", "N/A")

        report += f"Text: {text}\n"
        report += f"Sentiment: {sentiment}\n"
        report += "---\n"

    return report

if __name__ == "__main__":
    report = generate_report()
    print(report)
