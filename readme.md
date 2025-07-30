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


## Setting up Celery Beat
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

Note: When running in background you can use "docker logs <container_name_or_id>" to see the log and "docker ps" to find the ID.

## How to Create and Schedule a Task
1) Create a method for your task wherever you are working on it that can be called and complete the task. It should be in a package (ie there should be an \_\_init\_\_.py file in the same folder as the file you are working on).
2) Go to src/justinsight/tasks.py and create a new task following the format of the sample task. Remember to add an import statement if one is needed.
3) Go to src/justinsight/celery.py and schedule a new task after the comment showing where to schedule them. The new task can follow the same format as those above

   "sample-task-name": {  
        "task": "justinsight.tasks.your_task_name",  
        "schedule": x, #where x is the number of seconds between when the task should happen  
        "args": (), #potential arguments for your task  
    },


## How to check what's in the database
Please run: docker compose up -d --build
Then: docker exec -it mongo mongosh -u myuser -p mypassword  
Then: use justinsightdb
Then: db.articles.find().pretty()  
Note - you may need to download mongosh for this to work and to exit the mongosh environment just run 'exit'. Remember to 'docker compose down' as the containers will be running in the background.  
Note - to delete everything in your database run the docker in detached mode and then run ./scripts/clear_db.sh