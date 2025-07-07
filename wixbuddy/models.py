from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import EmailValidator
from django.utils import timezone
import uuid
import random
from datetime import timedelta

class User(AbstractUser):
    email = models.EmailField(unique=True, validators=[EmailValidator()])
    is_email_verified = models.BooleanField(default=False)
    agreed_to_policy = models.BooleanField(default=False)
    google_id = models.CharField(max_length=100, blank=True, null=True)
    apple_id = models.CharField(max_length=100, blank=True, null=True)
    # Override AbstractUser fields
    first_name = None  # Remove first_name
    last_name = None   # Remove last_name
    name = models.CharField(max_length=150, blank=True, null=True)
    family_name = models.CharField(max_length=150, blank=True, null=True)
    job_title = models.CharField(max_length=100, blank=True, null=True)
    current_company = models.CharField(max_length=100, blank=True, null=True)
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']
    
    def __str__(self):
        return self.email

class Question(models.Model):
    QUESTION_TYPES = [
        ('multiple_choice', 'Multiple Choice'),
        ('text', 'Text'),
    ]
    
    title = models.CharField(max_length=500)
    question_type = models.CharField(max_length=20, choices=QUESTION_TYPES, default='multiple_choice')
    options = models.JSONField(default=list, blank=True)  # For multiple choice options
    order = models.IntegerField(default=0)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['order']
    
    def __str__(self):
        return f"{self.order}. {self.title}"

class OTP(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    otp_code = models.CharField(max_length=6)
    is_used = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()
    
    def __str__(self):
        return f"OTP for {self.user.email}"
    
    @classmethod
    def generate_otp(cls):
        return ''.join([str(random.randint(0, 9)) for _ in range(6)])

class RefreshToken(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    token = models.CharField(max_length=255, unique=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()
    
    def __str__(self):
        return f"Refresh Token for {self.user.email}"
    
    @classmethod
    def generate_token(cls):
        return str(uuid.uuid4())
    
    def is_expired(self):
        return timezone.now() > self.expires_at
    
    def refresh_expiry(self):
        self.expires_at = timezone.now() + timedelta(days=30)
        self.save()

class AccessToken(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    refresh_token = models.ForeignKey(RefreshToken, on_delete=models.CASCADE)
    token = models.CharField(max_length=255, unique=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()
    
    def __str__(self):
        return f"Access Token for {self.user.email}"
    
    @classmethod
    def generate_token(cls):
        return str(uuid.uuid4())
    
    def is_expired(self):
        return timezone.now() > self.expires_at
    
    @classmethod
    def create_tokens(cls, user):
        # Create refresh token
        refresh_token = RefreshToken.objects.create(
            user=user,
            token=RefreshToken.generate_token(),
            expires_at=timezone.now() + timedelta(days=30)
        )
        
        # Create access token
        access_token = cls.objects.create(
            user=user,
            refresh_token=refresh_token,
            token=cls.generate_token(),
            expires_at=timezone.now() + timedelta(days=30)  # 30 days expiry
        )
        
        return access_token, refresh_token

class About(models.Model):
    bio = models.TextField()
    image = models.ImageField(upload_to='about_images/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"About ({self.created_at})"

class DashboardImage(models.Model):
    title = models.CharField(max_length=100)
    image = models.ImageField(upload_to='dashboard_images/')
    order = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.title

class SubscriptionPlan(models.Model):
    PLAN_TYPES = [
        ('basic', 'Basic'),
        ('pro', 'Pro'),
        ('premium', 'Premium'),
    ]
    
    BILLING_CYCLES = [
        ('monthly', 'Monthly'),
        ('yearly', 'Yearly'),
    ]
    
    name = models.CharField(max_length=100)
    plan_type = models.CharField(max_length=20, choices=PLAN_TYPES)
    billing_cycle = models.CharField(max_length=20, choices=BILLING_CYCLES)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stripe_price_id = models.CharField(max_length=100, unique=True)
    is_active = models.BooleanField(default=True)
    features = models.JSONField(default=list, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ['plan_type', 'billing_cycle']
    
    def __str__(self):
        return f"{self.name} - {self.billing_cycle}"

class UserSubscription(models.Model):
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('canceled', 'Canceled'),
        ('past_due', 'Past Due'),
        ('unpaid', 'Unpaid'),
        ('trialing', 'Trialing'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='subscriptions')
    plan = models.ForeignKey(SubscriptionPlan, on_delete=models.CASCADE)
    stripe_subscription_id = models.CharField(max_length=100, unique=True)
    stripe_customer_id = models.CharField(max_length=100)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='active')
    current_period_start = models.DateTimeField()
    current_period_end = models.DateTimeField()
    cancel_at_period_end = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.user.email} - {self.plan.name}"
    
    @property
    def is_active(self):
        return self.status in ['active', 'trialing']
    
    @property
    def days_until_renewal(self):
        from django.utils import timezone
        return (self.current_period_end - timezone.now()).days

class PaymentHistory(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='payments')
    subscription = models.ForeignKey(UserSubscription, on_delete=models.CASCADE, related_name='payments')
    stripe_payment_intent_id = models.CharField(max_length=100, unique=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    currency = models.CharField(max_length=3, default='usd')
    status = models.CharField(max_length=20)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.user.email} - {self.amount} {self.currency}"
