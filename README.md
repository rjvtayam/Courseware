# Courseware

A modern course management system built with Flask.

## Features
- Course Management
- User Authentication
- Real-time Updates with WebSocket
- Elasticsearch Integration
- File Upload Capabilities

## Tech Stack
- Flask 3.0.0
- Flask-SQLAlchemy
- Flask-Login
- Flask-SocketIO
- Elasticsearch
- MySQL/PostgreSQL

## Deployment
This application is configured for deployment on Render.com.

## Setup
1. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Set up environment variables in `.env`:
```
SECRET_KEY=your-secret-key
DATABASE_URL=your-database-url
ELASTICSEARCH_URL=your-elasticsearch-url
```

4. Run the application:
```bash
python run.py
```
