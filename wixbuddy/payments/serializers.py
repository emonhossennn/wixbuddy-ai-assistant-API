from rest_framework import serializers
from .models import SubscriptionPlan, UserSubscription, PaymentHistory

class SubscriptionPlanSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubscriptionPlan
        fields = '__all__'

class UserSubscriptionSerializer(serializers.ModelSerializer):
    plan = SubscriptionPlanSerializer(read_only=True)
    
    class Meta:
        model = UserSubscription
        fields = '__all__'

class CreateSubscriptionSerializer(serializers.Serializer):
    plan_id = serializers.IntegerField()
    success_url = serializers.URLField(required=False)
    cancel_url = serializers.URLField(required=False)

class CancelSubscriptionSerializer(serializers.Serializer):
    cancel_at_period_end = serializers.BooleanField(default=True)

class PaymentHistorySerializer(serializers.ModelSerializer):
    subscription = UserSubscriptionSerializer(read_only=True)
    
    class Meta:
        model = PaymentHistory
        fields = '__all__'

class SimplePaymentHistorySerializer(serializers.ModelSerializer):
    plan_name = serializers.CharField(source='subscription.plan.name', read_only=True)
    plan_price = serializers.CharField(source='subscription.plan.price', read_only=True)
    
    class Meta:
        model = PaymentHistory
        fields = ['id', 'amount', 'currency', 'status', 'created_at', 'plan_name', 'plan_price'] 