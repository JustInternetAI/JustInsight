# JustInsight

A lightweight, news intelligence service for ingesting free news sources, tagging entities & topics, extracting facts, and surfacing insights.

## ✅ MVP Features
- **Ingestion**: RSS & NewsAPI feeds
- **Normalization**: Store title, body, timestamp, source
- **NLP**: Entity Recognition, Topic Modeling, Fact Extraction
- **Insights**: Trend alerts, basic analytics dashboard

## 🛠️ Tech Stack
- **Backend**: Python + FastAPI
- **NLP**: spaCy, Hugging Face pipelines, BERTopic
- **Storage**: MongoDB or PostgreSQL (optional Elasticsearch)
- **Frontend**: Streamlit prototype
- **DevOps**: Docker, GitHub Actions CI

## 🚀 Getting Started
1. **Clone** the repo:
   ```bash
   git clone https://github.com/JustInternetAI/JustInsight.git
   cd justinsight


## Setting up Celery Beat:
- On MacOS
   - run: docker compose up --build
      - OR for running in the background: docker compose up -d
   - use local development section of entrypoint.sh
   - to shut down celery: docker compose down
- On the EC2
   - run: docker compose -f docker-compose.yml -f docker-compose.gpu.yml up --build
      - OR for running in the background: docker compose up -d
   - use EC2 section of entrypoint.sh
   - to shut down celery: docker compose down