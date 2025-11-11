from rest_framework import serializers
from .models import Conversation, Message, ConversationAnalysis

class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = ['sender', 'text']

class ConversationSerializer(serializers.ModelSerializer):
    messages = MessageSerializer(many=True, required=False)
    
    class Meta:
        model = Conversation
        fields = ['id', 'title', 'created_at', 'messages']
        read_only_fields = ['id', 'created_at']
    
    def create(self, validated_data):
        messages_data = validated_data.pop('messages', [])
        conversation = Conversation.objects.create(**validated_data)
        
        for message_data in messages_data:
            Message.objects.create(conversation=conversation, **message_data)
        
        return conversation

class ConversationAnalysisSerializer(serializers.ModelSerializer):
    class Meta:
        model = ConversationAnalysis
        fields = [
            'clarity_score', 'relevance_score', 'sentiment',
            'empathy_score', 'accuracy_score', 'completeness_score',
            'response_time_avg', 'resolution_score', 'escalation_needed',
            'fallback_count', 'overall_score', 'created_at'
        ]