# Celery Configuration
# Using memory broker for local development
CELERY_BROKER_URL = 'memory://'
CELERY_RESULT_BACKEND = 'cache+memory://'
CELERY_CACHE_BACKEND = 'django.core.cache.backends.locmem.LocMemCache'
CELERY_ACCEPT_CONTENT = ['json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
CELERY_TIMEZONE = 'UTC'

# Celery Beat Schedule
CELERY_BEAT_SCHEDULE = {
    'analyze-new-conversations': {
        'task': 'chat_analysis.tasks.analyze_new_conversations',
        'schedule': 86400.0,  # Daily
    },
}