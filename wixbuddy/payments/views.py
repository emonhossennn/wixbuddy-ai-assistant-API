from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status
from django.http import HttpResponse
import json
import stripe
from .models import SubscriptionPlan, UserSubscription, PaymentHistory
from .serializers import (
    SubscriptionPlanSerializer, UserSubscriptionSerializer, 
    CreateSubscriptionSerializer, CancelSubscriptionSerializer, 
    PaymentHistorySerializer, SimplePaymentHistorySerializer
)
from .services import StripeService
from wixbuddy.authentication import IsAuthenticated
import os

@api_view(['GET'])
@permission_classes([AllowAny])
def subscription_plans(request):
    """Get all available subscription plans"""
    plans = SubscriptionPlan.objects.filter(is_active=True)
    serializer = SubscriptionPlanSerializer(plans, many=True)
    return Response(serializer.data)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_subscription(request):
    """Create a new subscription checkout session"""
    try:
        serializer = CreateSubscriptionSerializer(data=request.data)
        if serializer.is_valid():
            plan_id = serializer.validated_data['plan_id']
            success_url = serializer.validated_data.get('success_url', 'http://localhost:3000/success')
            cancel_url = serializer.validated_data.get('cancel_url', 'http://localhost:3000/cancel')
            
            try:
                plan = SubscriptionPlan.objects.get(id=plan_id, is_active=True)
                
                # Create Stripe price if it doesn't exist
                if not plan.stripe_price_id:
                    try:
                        StripeService.create_price(plan)
                    except Exception as e:
                        return Response({'error': f'Failed to create Stripe price: {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
                        
            except SubscriptionPlan.DoesNotExist:
                return Response({'error': 'Plan not found'}, status=status.HTTP_404_NOT_FOUND)
            
            # Check if user already has an active subscription
            existing_subscription = UserSubscription.objects.filter(
                user=request.user, 
                status__in=['active', 'trialing']
            ).first()
            
            if existing_subscription:
                return Response({
                    'error': 'User already has an active subscription'
                }, status=status.HTTP_400_BAD_REQUEST)
            
            # Create checkout session
            checkout_session = StripeService.create_checkout_session(
                user=request.user,
                plan=plan,
                success_url=success_url,
                cancel_url=cancel_url
            )
            
            return Response({
                'checkout_url': checkout_session.url,
                'session_id': checkout_session.id
            })
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def subscription_status(request):
    """Get current user's subscription status"""
    try:
        subscription = UserSubscription.objects.filter(
            user=request.user
        ).order_by('-created_at').first()
        
        if subscription:
            serializer = UserSubscriptionSerializer(subscription)
            return Response(serializer.data)
        else:
            return Response({'message': 'No active subscription found'})
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def cancel_subscription(request):
    """Cancel user's subscription"""
    try:
        serializer = CancelSubscriptionSerializer(data=request.data)
        if serializer.is_valid():
            cancel_at_period_end = serializer.validated_data['cancel_at_period_end']
            
            subscription = UserSubscription.objects.filter(
                user=request.user,
                status__in=['active', 'trialing']
            ).first()
            
            if not subscription:
                return Response({
                    'error': 'No active subscription found'
                }, status=status.HTTP_404_NOT_FOUND)
            
            # Cancel in Stripe
            StripeService.cancel_subscription(
                subscription.stripe_subscription_id,
                cancel_at_period_end
            )
            
            # Update local subscription
            if cancel_at_period_end:
                subscription.cancel_at_period_end = True
                subscription.save()
                message = 'Subscription will be canceled at the end of the current period'
            else:
                subscription.status = 'canceled'
                subscription.save()
                message = 'Subscription canceled immediately'
            
            return Response({'message': message})
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def payment_history(request):
    """Get user's payment history"""
    try:
        payments = PaymentHistory.objects.filter(user=request.user).order_by('-created_at')
        serializer = SimplePaymentHistorySerializer(payments, many=True)
        return Response(serializer.data)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['POST'])
@permission_classes([AllowAny])
def stripe_webhook(request):
    """Handle Stripe webhook events"""
    try:
        payload = request.body
        sig_header = request.META.get('HTTP_STRIPE_SIGNATURE')
        
        # Verify webhook signature
        try:
            event = stripe.Webhook.construct_event(
                payload, sig_header, os.getenv('STRIPE_WEBHOOK_SECRET', '')
            )
        except ValueError as e:
            return HttpResponse(status=400)
        except stripe.error.SignatureVerificationError as e:
            return HttpResponse(status=400)
        
        # Handle the event
        StripeService.handle_webhook_event(event)
        
        return HttpResponse(status=200)
    except Exception as e:
        return HttpResponse(status=500) 