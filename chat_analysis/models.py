from django.db import models

class Conversation(models.Model):
    title = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

class Message(models.Model):
    conversation = models.ForeignKey(Conversation, on_delete=models.CASCADE, related_name="messages")
    sender = models.CharField(max_length=20)  # "user" or "ai"
    text = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.sender}: {self.text[:50]}..."

class ConversationAnalysis(models.Model):
    conversation = models.OneToOneField(Conversation, on_delete=models.CASCADE, related_name="analysis")
    clarity_score = models.FloatField()
    relevance_score = models.FloatField()
    sentiment = models.CharField(max_length=20)
    empathy_score = models.FloatField()
    accuracy_score = models.FloatField()
    completeness_score = models.FloatField()
    response_time_avg = models.FloatField()  # in seconds
    resolution_score = models.FloatField()
    escalation_needed = models.BooleanField(default=False)
    fallback_count = models.IntegerField(default=0)
    overall_score = models.FloatField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Analysis for {self.conversation.title}"
