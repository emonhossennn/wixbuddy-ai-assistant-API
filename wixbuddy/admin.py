from django.contrib import admin
from .models import About, DashboardImage, SubscriptionPlan, UserSubscription, PaymentHistory

admin.site.register(About)
admin.site.register(DashboardImage)

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