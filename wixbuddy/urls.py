"""
URL configuration for wixbuddy project.
"""
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views
from .views import AboutAPIView

# API Router for ViewSets
router = DefaultRouter()
router.register(r'questions', views.QuestionViewSet)

# URL Patterns
urlpatterns = [
    path('api/auth/signup/', views.signup, name='signup'),
    path('api/auth/signin/', views.signin, name='signin'),
    path('api/auth/refresh/', views.refresh, name='refresh'),
    path('api/auth/logout/', views.logout, name='logout'),
    path('api/auth/profile/', views.profile, name='profile'),
    path('api/auth/forgot-password/', views.forgot_password, name='forgot_password'),
    path('api/auth/reset-password/', views.reset_password, name='reset_password'),
    path('api/auth/google/', views.google_signin, name='google_signin'),
    path('api/auth/apple/', views.apple_signin, name='apple_signin'),
    # Dashboard and question endpoints
    path('api/dashboard/', views.dashboard, name='dashboard_api'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('api/', include(router.urls)),  # This will include questions endpoints
    path('api/about', AboutAPIView.as_view(), name='about_api'),
    # Account Settings endpoint
    path('api/account-settings/', views.account_settings, name='account_settings'),
    # Subscription endpoints
    path('api/subscription/plans/', views.subscription_plans, name='subscription_plans'),
    path('api/subscription/create/', views.create_subscription, name='create_subscription'),
    path('api/subscription/status/', views.subscription_status, name='subscription_status'),
    path('api/subscription/cancel/', views.cancel_subscription, name='cancel_subscription'),
    path('api/subscription/payments/', views.payment_history, name='payment_history'),
    path('api/webhook/stripe/', views.stripe_webhook, name='stripe_webhook'),
    path('', views.home, name='home'),
] 