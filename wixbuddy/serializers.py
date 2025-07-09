from rest_framework import serializers
from .models import Question, User, About, SubscriptionPlan, UserSubscription, PaymentHistory, Resource, Video, FAQ, ChatMessage, ChatSession

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email', 'name', 'family_name', 'is_email_verified', 'job_title', 'current_company']
        read_only_fields = ['id', 'is_email_verified']

class SignUpSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)
    confirm_password = serializers.CharField(write_only=True)
    agreed_to_policy = serializers.BooleanField()

    def validate(self, attrs):
        if attrs['password'] != attrs['confirm_password']:
            raise serializers.ValidationError({"confirm_password": "Passwords do not match."})
        return attrs

class SignInSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

class ForgotPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField()

class ResetPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField()
    otp = serializers.CharField(max_length=6)
    new_password = serializers.CharField(write_only=True)

class GoogleSignInSerializer(serializers.Serializer):
    token = serializers.CharField()

class AppleSignInSerializer(serializers.Serializer):
    token = serializers.CharField()

class TokenInfoSerializer(serializers.Serializer):
    access = serializers.CharField()
    refresh = serializers.CharField()
    expires_in = serializers.IntegerField()

class AuthResponseSerializer(serializers.Serializer):
    user = UserSerializer()
    tokens = TokenInfoSerializer()

class RefreshTokenRequestSerializer(serializers.Serializer):
    refresh = serializers.CharField()

class RefreshTokenResponseSerializer(serializers.Serializer):
    access = serializers.CharField()
    expires_in = serializers.IntegerField()

class LogoutResponseSerializer(serializers.Serializer):
    message = serializers.CharField()

class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = ['id', 'title', 'options', 'order', 'is_active', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']

# Dashboard-specific serializers
# Removed DashboardUserSerializer, DashboardDataSerializer, DashboardResponseSerializer

class ErrorResponseSerializer(serializers.Serializer):
    """Serializer for error responses"""
    error = serializers.CharField()

class SuccessResponseSerializer(serializers.Serializer):
    """Serializer for success responses"""
    message = serializers.CharField()

class AboutSerializer(serializers.ModelSerializer):
    imageUrl = serializers.SerializerMethodField()

    class Meta:
        model = About
        fields = ['bio', 'imageUrl']

    def get_imageUrl(self, obj):
        request = self.context.get('request')
        if obj.image and hasattr(obj.image, 'url'):
            return request.build_absolute_uri(obj.image.url) if request else obj.image.url
        return ''

class SubscriptionPlanSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubscriptionPlan
        fields = ['id', 'name', 'plan_type', 'billing_cycle', 'price', 'features', 'is_active']

class UserSubscriptionSerializer(serializers.ModelSerializer):
    plan = SubscriptionPlanSerializer(read_only=True)
    days_until_renewal = serializers.ReadOnlyField()
    
    class Meta:
        model = UserSubscription
        fields = [
            'id', 'plan', 'status', 'current_period_start', 'current_period_end',
            'cancel_at_period_end', 'is_active', 'days_until_renewal', 'created_at'
        ]

class CreateSubscriptionSerializer(serializers.Serializer):
    plan_id = serializers.IntegerField()
    success_url = serializers.URLField()
    cancel_url = serializers.URLField()

class CancelSubscriptionSerializer(serializers.Serializer):
    cancel_at_period_end = serializers.BooleanField(default=True)

class PaymentHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = PaymentHistory
        fields = ['id', 'amount', 'currency', 'status', 'created_at']
        read_only_fields = ['id', 'created_at']

class AccountSettingsSerializer(serializers.ModelSerializer):
    """Serializer for account settings - allows updating profile information"""
    class Meta:
        model = User
        fields = ['name', 'family_name', 'email', 'job_title', 'current_company']
        read_only_fields = ['email']  # Email should not be changed via this endpoint

class ChangePasswordSerializer(serializers.Serializer):
    """Serializer for changing password"""
    current_password = serializers.CharField(write_only=True)
    new_password = serializers.CharField(write_only=True, min_length=8)
    confirm_password = serializers.CharField(write_only=True)

    def validate(self, attrs):
        if attrs['new_password'] != attrs['confirm_password']:
            raise serializers.ValidationError("New passwords don't match.")
        return attrs

    def validate_new_password(self, value):
        # Add password strength validation if needed
        if len(value) < 8:
            raise serializers.ValidationError("Password must be at least 8 characters long.")
        return value

class VideoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Video
        fields = ['id', 'title', 'file', 'uploaded_at']

class FAQSerializer(serializers.ModelSerializer):
    class Meta:
        model = FAQ
        fields = ['id', 'question', 'answer']

class ResourceSerializer(serializers.ModelSerializer):
    videos = VideoSerializer(many=True, read_only=True)
    faqs = FAQSerializer(many=True, read_only=True)

    class Meta:
        model = Resource
        fields = ['id', 'name', 'description', 'created_at', 'videos', 'faqs']

class MinimalQuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = ['title', 'options']

# Chatbot Serializers
class ChatMessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChatMessage
        fields = ['id', 'sender', 'content', 'timestamp']

class ChatSessionSerializer(serializers.ModelSerializer):
    messages = ChatMessageSerializer(many=True, read_only=True)
    
    class Meta:
        model = ChatSession
        fields = ['id', 'user', 'start_time', 'end_time', 'messages']
