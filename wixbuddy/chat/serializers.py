from rest_framework import serializers
from .models import ChatSession, ChatMessage

class ChatMessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChatMessage
        fields = ['id', 'sender', 'content', 'timestamp']

class ChatSessionSerializer(serializers.ModelSerializer):
    messages = ChatMessageSerializer(many=True, read_only=True)
    
    class Meta:
        model = ChatSession
        fields = ['id', 'start_time', 'end_time', 'messages']

class ChatRequestSerializer(serializers.Serializer):
    message = serializers.CharField(max_length=10000)

class ChatHistoryResponseSerializer(serializers.Serializer):
    history = ChatSessionSerializer(many=True)
    total_sessions = serializers.IntegerField() 