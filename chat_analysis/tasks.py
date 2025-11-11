from celery import shared_task
from .models import Conversation
from .services import ConversationAnalyzer

@shared_task
def analyze_new_conversations():
    # Get conversations that don't have analysis yet
    conversations = Conversation.objects.filter(analysis__isnull=True)
    analyzer = ConversationAnalyzer()
    
    for conversation in conversations:
        analyzer.analyze_conversation(conversation)
    
    return f"Analyzed {len(conversations)} new conversations"