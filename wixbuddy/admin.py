from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html
from .models import About, DashboardImage, SubscriptionPlan, UserSubscription, PaymentHistory, Resource, Video, FAQ, Question, ChatSession, ChatMessage
from adminsortable2.admin import SortableAdminMixin

admin.site.register(About)
admin.site.register(DashboardImage)

class VideoInline(admin.TabularInline):
    model = Video
    extra = 1

class FAQInline(admin.TabularInline):
    model = FAQ
    extra = 1

@admin.register(Resource)
class ResourceAdmin(admin.ModelAdmin):
    inlines = [VideoInline, FAQInline]
    list_display = ['name', 'created_at']

@admin.register(SubscriptionPlan)
class SubscriptionPlanAdmin(admin.ModelAdmin):
    list_display = ['name', 'plan_type', 'billing_cycle', 'price', 'is_active']
    list_filter = ['plan_type', 'billing_cycle', 'is_active']
    search_fields = ['name', 'stripe_price_id']

@admin.register(UserSubscription)
class UserSubscriptionAdmin(admin.ModelAdmin):
    list_display = ['user', 'plan', 'status', 'current_period_end', 'is_active']
    list_filter = ['status', 'plan__plan_type', 'cancel_at_period_end']
    search_fields = ['user__email', 'stripe_subscription_id']
    readonly_fields = ['stripe_subscription_id', 'stripe_customer_id']

@admin.register(PaymentHistory)
class PaymentHistoryAdmin(admin.ModelAdmin):
    list_display = ['user', 'subscription', 'amount', 'currency', 'status', 'created_at']
    list_filter = ['status', 'currency', 'created_at']
    search_fields = ['user__email', 'stripe_payment_intent_id']
    readonly_fields = ['stripe_payment_intent_id']

admin.site.register(Video)
admin.site.register(FAQ)

# Remove the default registration for Question
from django.contrib import admin
try:
    admin.site.unregister(Question)
except admin.sites.NotRegistered:
    pass

@admin.register(Question)
class QuestionAdmin(SortableAdminMixin, admin.ModelAdmin):
    list_display = ('order', 'title', 'options', 'is_active', 'created_at')
    list_editable = ('title', 'options', 'is_active')  # Do NOT include 'order'
    ordering = ('order',)
    search_fields = ('title',)
    list_display_links = ()  # No clickable links, just drag handle for order
    # Optionally, add list_filter if needed
    # list_filter = ('is_active',)

# Chatbot Admin
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