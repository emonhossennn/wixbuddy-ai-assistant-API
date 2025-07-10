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
    title = models.CharField(max_length=500)
    options = models.JSONField(default=list, blank=True)  # For multiple choice options
    order = models.PositiveIntegerField(default=0, unique=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['order']
        verbose_name = 'Survey Question'
        verbose_name_plural = 'Survey Questions'
    
    def __str__(self):
        return f"{self.order}. {self.title}"
    
    def clean(self):
        from django.core.exceptions import ValidationError
        if self.order < 0:
            raise ValidationError({'order': 'Order must be a positive integer.'})
        # Check for duplicate order
        qs = Question.objects.exclude(pk=self.pk).filter(order=self.order)
        if qs.exists():
            raise ValidationError({'order': 'Order must be unique.'})
    
    def save(self, *args, **kwargs):
        is_new = self.pk is None
        super().save(*args, **kwargs)  # Save first to get a PK if new
        # Reorder all questions to ensure continuous order and correct titles
        questions = Question.objects.all().order_by('order', 'pk')
        for idx, q in enumerate(questions, start=1):
            if q.order != idx or not q.title.startswith(f"{idx}."):
                q.order = idx
                q.title = f"{idx}. {q.title.lstrip('0123456789. ')}"
                super(Question, q).save(update_fields=['order', 'title'])

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



class Resource(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class Video(models.Model):
    resource = models.ForeignKey(Resource, on_delete=models.CASCADE, related_name='videos')
    title = models.CharField(max_length=255)
    file = models.FileField(upload_to='videos/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} ({self.resource.name})"

class FAQ(models.Model):
    resource = models.ForeignKey(Resource, on_delete=models.CASCADE, related_name='faqs')
    question = models.CharField(max_length=255)
    answer = models.TextField()

    def __str__(self):
        return f"FAQ for {self.resource.name}: {self.question}"


# Add after existing models
class BlogCategory(models.Model):
    name = models.CharField(max_length=100, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = 'Blog Categories'

    def __str__(self):
        return self.name

class Blog(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    category = models.ForeignKey(BlogCategory, on_delete=models.CASCADE, related_name='blogs')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

# Chatbot Models

