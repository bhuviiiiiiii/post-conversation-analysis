# Post-Conversation Analysis

A Django REST Framework application that performs automated analysis on AI-human conversations and stores results in a database.

## 📋 Features

- **Post-conversation analysis** of chat messages between AI and humans
- **10+ analysis parameters** including clarity, relevance, sentiment, empathy, and more
- **REST API endpoints** for conversation upload and analysis retrieval
- **Automated daily analysis** using Celery Beat (configurable scheduling)
- **Database integration** with SQLite (easily switch to PostgreSQL for production)
- **Admin interface** for managing conversations and analysis results

## 🎯 Analysis Parameters

The application analyzes conversations on the following metrics:

| Category | Parameter | Description |
|----------|-----------|-------------|
| **Conversation Quality** | Clarity | Response clarity and readability score |
| | Relevance | How well AI stayed on topic |
| | Accuracy | Factual correctness of responses |
| | Completeness | Sufficiency of answers |
| **Interaction** | Sentiment | User sentiment (positive/neutral/negative) |
| | Empathy | Empathetic tone in AI responses |
| | Response Time | Average time between messages |
| **Resolution** | Resolution Score | Issue resolution indicator |
| | Escalation Need | Whether escalation to human is needed |
| **AI Operations** | Fallback Count | Instances of "I don't know" responses |
| **Overall** | Overall Score | Weighted average of key parameters |

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- pip / virtualenv

### Installation

1. **Clone the repository**
```bash
git clone https://github.com/<your-username>/post-conversation-analysis
cd post-conversation-analysis
```

2. **Create and activate virtual environment**
```bash
python -m venv venv
# On Windows:
.\venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Run database migrations**
```bash
python manage.py makemigrations
python manage.py migrate
```

5. **Create a superuser (optional, for admin access)**
```bash
python manage.py createsuperuser
```

### Running the Application

**Terminal 1: Start Django Development Server**
```bash
python manage.py runserver
```
The server will be available at `http://127.0.0.1:8000/`

**Terminal 2: Start Celery Worker**
```bash
celery -A post_analysis worker -l info
```

**Terminal 3: Start Celery Beat (Scheduler)**
```bash
celery -A post_analysis beat -l info
```

Or run worker and beat together:
```bash
celery -A post_analysis worker -B -l info
```

## 🔌 API Documentation

### Base URL
```
http://127.0.0.1:8000/api/
```

### 1. Upload a Conversation

**Endpoint:** `POST /api/conversations/`

**Request:**
```bash
curl -X POST http://127.0.0.1:8000/api/conversations/ \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Customer Support Chat",
    "messages": [
      {
        "sender": "user",
        "text": "Hi, I need help with my order."
      },
      {
        "sender": "ai",
        "text": "Sure, can you please share your order ID?"
      },
      {
        "sender": "user",
        "text": "It'\''s 12345."
      },
      {
        "sender": "ai",
        "text": "Thanks! Your order has been shipped and will arrive tomorrow."
      }
    ]
  }'
```

**Response (201 Created):**
```json
{
  "conversation": {
    "id": 1,
    "title": "Customer Support Chat",
    "created_at": "2025-11-11T09:07:11.993158Z",
    "messages": [
      {
        "sender": "user",
        "text": "Hi, I need help with my order."
      },
      {
        "sender": "ai",
        "text": "Sure, can you please share your order ID?"
      }
    ]
  },
  "analysis": {
    "clarity_score": 1.0,
    "relevance_score": 0.0625,
    "sentiment": "neutral",
    "empathy_score": 0.3333333333333333,
    "accuracy_score": 0.85,
    "completeness_score": 0.3333333333333333,
    "response_time_avg": 0.013347,
    "resolution_score": 0.0,
    "escalation_needed": false,
    "fallback_count": 0,
    "overall_score": 0.4298611111111111,
    "created_at": "2025-11-11T09:07:51.344657Z"
  }
}
```

### 2. Get All Analysis Reports

**Endpoint:** `GET /api/reports/`

**Request:**
```bash
curl -X GET http://127.0.0.1:8000/api/reports/
```

**Response (200 OK):**
```json
[
  {
    "clarity_score": 1.0,
    "relevance_score": 0.0625,
    "sentiment": "neutral",
    "empathy_score": 0.3333333333333333,
    "accuracy_score": 0.85,
    "completeness_score": 0.3333333333333333,
    "response_time_avg": 0.013347,
    "resolution_score": 0.0,
    "escalation_needed": false,
    "fallback_count": 0,
    "overall_score": 0.4298611111111111,
    "created_at": "2025-11-11T09:07:51.344657Z"
  }
]
```

### 3. Analyze Specific Conversation

**Endpoint:** `POST /api/conversations/{id}/analyze/`

**Request:**
```bash
curl -X POST http://127.0.0.1:8000/api/conversations/1/analyze/
```

**Response (200 OK):**
```json
{
  "clarity_score": 1.0,
  "relevance_score": 0.0625,
  "sentiment": "neutral",
  "empathy_score": 0.3333333333333333,
  "accuracy_score": 0.85,
  "completeness_score": 0.3333333333333333,
  "response_time_avg": 0.013347,
  "resolution_score": 0.0,
  "escalation_needed": false,
  "fallback_count": 0,
  "overall_score": 0.4298611111111111,
  "created_at": "2025-11-11T09:07:51.344657Z"
}
```

### 4. List All Conversations

**Endpoint:** `GET /api/conversations/`

**Response (200 OK):**
```json
[
  {
    "id": 1,
    "title": "Customer Support Chat",
    "created_at": "2025-11-11T09:07:11.993158Z",
    "messages": [...]
  }
]
```

## ⏰ Cron Job / Scheduled Tasks

### Setup with Celery Beat

The application automatically analyzes new conversations once per day using Celery Beat.

**Schedule Configuration** in `post_analysis/celery_settings.py`:
```python
CELERY_BEAT_SCHEDULE = {
    'analyze-new-conversations': {
        'task': 'chat_analysis.tasks.analyze_new_conversations',
        'schedule': 86400.0,  # 24 hours in seconds
    },
}
```

**To modify the schedule:**
1. Edit `post_analysis/celery_settings.py`
2. Change the `'schedule'` value (in seconds):
   - `3600.0` = 1 hour
   - `86400.0` = 1 day
   - `604800.0` = 1 week

**To trigger analysis manually:**
```bash
python manage.py shell
>>> from chat_analysis.tasks import analyze_new_conversations
>>> analyze_new_conversations.delay()
```

## 📦 Project Structure

```
post-conversation-analysis/
├── manage.py                    # Django management script
├── requirements.txt             # Python dependencies
├── README.md                    # This file
├── db.sqlite3                   # SQLite database (dev only)
├── venv/                        # Virtual environment
│
├── post_analysis/               # Main Django project
│   ├── settings.py              # Django settings
│   ├── urls.py                  # URL routing
│   ├── wsgi.py                  # WSGI app for deployment
│   ├── celery.py                # Celery app initialization
│   └── celery_settings.py       # Celery configuration
│
└── chat_analysis/               # Main app
    ├── models.py                # Database models
    ├── views.py                 # REST API views
    ├── serializers.py           # API serializers
    ├── services.py              # Analysis logic
    ├── tasks.py                 # Celery tasks
    ├── urls.py                  # App URL routes
    ├── admin.py                 # Django admin
    └── migrations/              # Database migrations
```

## 🛠️ Configuration

### Change Database (PostgreSQL for Production)

1. **Install PostgreSQL driver:**
```bash
pip install psycopg2-binary
```

2. **Update `post_analysis/settings.py`:**
```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'post_analysis_db',
        'USER': 'postgres',
        'PASSWORD': 'your-password',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
```

3. **Run migrations:**
```bash
python manage.py migrate
```

### Change Celery Broker (for Production)

For Redis broker (recommended for production):

1. **Install Redis:**
```bash
# macOS
brew install redis

# Linux (Ubuntu)
sudo apt-get install redis-server

# Windows (using WSL or Docker)
docker run -d -p 6379:6379 redis:latest
```

2. **Update `post_analysis/celery_settings.py`:**
```python
CELERY_BROKER_URL = 'redis://localhost:6379/0'
CELERY_RESULT_BACKEND = 'redis://localhost:6379/0'
```

## 🐳 Docker Deployment (Production)

Create a `Dockerfile`:
```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

RUN python manage.py collectstatic --noinput

EXPOSE 8000

CMD ["gunicorn", "post_analysis.wsgi", "--bind", "0.0.0.0:8000"]
```

Build and run:
```bash
docker build -t post-analysis .
docker run -p 8000:8000 -e DATABASE_URL=postgresql://... post-analysis
```

## 🧪 Testing

Run the included test script:
```bash
python test_api.py
```

This will:
1. Upload a sample conversation
2. Retrieve all analysis reports

## 📝 Analysis Algorithm Details

### Clarity Score
- Based on sentence structure and average word count per sentence
- Optimal range: 15-25 words per sentence
- Range: 0.0 - 1.0

### Relevance Score
- Calculates word overlap between user questions and AI responses
- Uses TextBlob for natural language processing
- Range: 0.0 - 1.0

### Sentiment Analysis
- Analyzes user message sentiment using TextBlob
- Returns: "positive", "neutral", or "negative"

### Empathy Score
- Counts empathy indicators: "understand", "sorry", "help", "thank you", etc.
- Range: 0.0 - 1.0

### Resolution Score
- Checks for resolution indicators in final messages
- Indicators: "solved", "resolved", "thanks", "great", etc.
- Returns: 0.0 or 1.0

### Escalation Needed
- Detects frustration indicators: "not working", "frustrated", "angry", etc.
- Returns: true or false

### Fallback Count
- Counts instances of "I don't know", "I can't", "unable to", etc.
- Returns: integer count

## 🐛 Troubleshooting

### Celery Worker Not Starting
- Ensure memory broker is configured in `celery_settings.py`
- Check that all Python dependencies are installed: `pip install -r requirements.txt`
- Verify Django settings are correctly set: `export DJANGO_SETTINGS_MODULE=post_analysis.settings`

### Database Errors
- Run migrations: `python manage.py migrate`
- Check database configuration in `settings.py`

### API Returns 400 Errors
- Verify JSON structure matches the examples above
- Ensure messages use `"text"` key, not `"message"`
- Both `sender` values must be either `"user"` or `"ai"`

## 📚 Dependencies

- **Django 4.2.7** - Web framework
- **Django REST Framework 3.14.0** - REST API toolkit
- **Celery 5.3.6** - Task queue
- **Django Celery Beat 2.5.0** - Celery scheduler
- **NLTK 3.8.1** - Natural language processing
- **TextBlob 0.17.1** - Text analysis
- **Gunicorn 21.2.0** - Production WSGI server

## 📄 License

MIT License - see LICENSE file for details

## 👤 Author

Bhuvnesh Choudhary / bhuviiiiiiii

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📞 Support

For issues and questions, please open an issue on GitHub or contact the maintainer.
