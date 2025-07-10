from django.urls import path
from . import views

app_name = 'payments'

urlpatterns = [
    path('plans/', views.subscription_plans, name='subscription_plans'),
    path('create/', views.create_subscription, name='create_subscription'),
    path('status/', views.subscription_status, name='subscription_status'),
    path('cancel/', views.cancel_subscription, name='cancel_subscription'),
    path('payments/', views.payment_history, name='payment_history'),
    path('webhook/stripe/', views.stripe_webhook, name='stripe_webhook'),
] 