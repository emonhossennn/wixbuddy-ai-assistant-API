from django.contrib import admin
from .models import ChatSession, ChatMessage

class ChatMessageInline(admin.TabularInline):
    model = ChatMessage
    extra = 0
    readonly_fields = ['timestamp']
    fields = ['sender', 'content', 'timestamp']

@admin.register(ChatSession)
class ChatSessionAdmin(admin.ModelAdmin):
    list_display = ['user', 'start_time', 'end_time', 'message_count']
    list_filter = ['start_time', 'end_time']
    search_fields = ['user__email']
    readonly_fields = ['start_time']
    inlines = [ChatMessageInline]
    
    def message_count(self, obj):
        return obj.messages.count()
    message_count.short_description = 'Messages'

@admin.register(ChatMessage)
class ChatMessageAdmin(admin.ModelAdmin):
    list_display = ['session', 'sender', 'content_preview', 'timestamp']
    list_filter = ['sender', 'timestamp']
    search_fields = ['content', 'session__user__email']
    readonly_fields = ['timestamp']
    
    def content_preview(self, obj):
        return obj.content[:100] + '...' if len(obj.content) > 100 else obj.content
    content_preview.short_description = 'Content' 