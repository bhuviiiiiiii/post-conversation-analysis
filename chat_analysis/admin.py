from django.contrib import admin
from .models import Conversation, Message, ConversationAnalysis

@admin.register(Conversation)
class ConversationAdmin(admin.ModelAdmin):
    list_display = ('title', 'created_at')
    search_fields = ('title',)

@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('conversation', 'sender', 'timestamp')
    list_filter = ('sender', 'timestamp')
    search_fields = ('text',)

@admin.register(ConversationAnalysis)
class ConversationAnalysisAdmin(admin.ModelAdmin):
    list_display = ('conversation', 'sentiment', 'overall_score', 'created_at')
    list_filter = ('sentiment', 'escalation_needed')
    search_fields = ('conversation__title',)
