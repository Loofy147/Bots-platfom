# Lucidya-like PoC

This repository contains a Proof-of-Concept (PoC) for a Lucidya-like Voice-of-Customer (VoC) and Social Listening platform. It provides a complete, integrated architecture using open-source components.

## Goals

* Ingest public social media data, customer feedback (surveys, messages), and call center recordings.
* Transcribe audio to text (ASR) and run NLP pipelines for sentiment, entity, and topic analysis.
* Store, index, and search text and metadata in OpenSearch.
* Provide an agent-facing inbox and ticketing system (Chatwoot).
* Expose dashboards, alerts, and reports (OpenSearch Dashboards / Metabase).

## High-level Architecture

The architecture is designed to be modular, allowing any component to be replaced with a proprietary or cloud-based alternative. The core components are:

* **Data Sources**: Social media APIs, contact center recordings, surveys, etc.
* **Ingest Layer**: Connectors to pull data from various sources.
* **Message Bus**: Redis or Kafka for queuing and decoupling services.
* **ASR/Speech-to-Text**: Whisper.cpp or VOSK for audio transcription.
* **NLP Workers**: CAMeL Tools, BERTopic, and Hugging Face Transformers for text enrichment.
* **Datastore**: OpenSearch for indexing and searching text data.
* **Agent Interface**: Chatwoot for omnichannel support and ticketing.
* **Dashboards & Reporting**: OpenSearch Dashboards or Metabase for data visualization.
* **CRM/Actioning**: SuiteCRM or Odoo for turning insights into actions.

## Getting Started

### Prerequisites

* Docker and Docker Compose
* Git

### Setup

1. **Clone the repository:**
   ```bash
   git clone <repository-url>
   cd lucidya-poc
   ```

2. **Configure the environment:**
   Create a `.env` file from the example file:
   ```bash
   cp .env.example .env
   ```
   Update the `.env` file with your own secrets. You can generate a `SECRET_KEY_BASE` for Chatwoot with `openssl rand -hex 64`.

3. **Start the services:**
   ```bash
   docker-compose up --build -d
   ```

4. **Initialize Chatwoot:**
   Run the database migrations for Chatwoot:
   ```bash
   docker-compose exec chatwoot rails db:chatwoot_prepare
   ```

### Accessing the Services

* **Chatwoot**: [http://localhost:3000](http://localhost:3000)
* **OpenSearch**: [http://localhost:9200](http://localhost:9200)
* **OpenSearch Dashboards**: [http://localhost:5601](http://localhost:5601)
* **NLP Worker**: [http://localhost:8000](http://localhost:8000)

### Ingesting Sample Data

To test the pipeline, you can send the sample data to the `nlp-worker`'s `/ingest` endpoint using the following `curl` command:

```bash
curl -X POST -H "Content-Type: application/json" -d @data/incoming/sample_data.json http://localhost:8000/ingest
```

This will send the contents of the `sample_data.json` file to the `nlp-worker`, which will then process it and index it into OpenSearch.

## Project Structure

* `.github/workflows/`: Contains CI/CD workflows.
* `data/`: Sample data for testing the pipeline.
* `nlp-worker/`: The NLP processing service.
* `docker-compose.yml`: Defines the services for the PoC.
* `README.md`: This file.
