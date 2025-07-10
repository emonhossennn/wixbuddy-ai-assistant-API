"""
URL configuration for wixbuddy project.
"""
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views
from .views import AboutAPIView, ResourceDetailView, QuestionsAPIView, QuestionViewSet

# API Router for ViewSets
router = DefaultRouter()
router.register(r'questions', QuestionViewSet)

# URL Patterns
from django.urls import path
from . import views

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
    # Include payment and chat module URLs
    path('api/subscription/', include('wixbuddy.payments.urls')),
    path('api/chatbot/', include('wixbuddy.chat.urls')),
    path('api/resources/<int:pk>/', ResourceDetailView.as_view(), name='resource-detail'),
    path('api/questions/', QuestionsAPIView.as_view(), name='questions-api'),
    path('', views.home, name='home'),
]