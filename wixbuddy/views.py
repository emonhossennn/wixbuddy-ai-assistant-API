from django.http import HttpResponse
from django.shortcuts import render, redirect
from rest_framework import viewsets, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from django.utils import timezone
from .models import Question, User, AccessToken, RefreshToken, About, DashboardImage, SubscriptionPlan, UserSubscription, PaymentHistory
from .serializers import (
    QuestionSerializer, ErrorResponseSerializer, SuccessResponseSerializer,
    UserSerializer, SignUpSerializer, SignInSerializer, ForgotPasswordSerializer, ResetPasswordSerializer,
    GoogleSignInSerializer, AppleSignInSerializer, TokenInfoSerializer, AuthResponseSerializer,
    RefreshTokenRequestSerializer, RefreshTokenResponseSerializer, LogoutResponseSerializer,
    AboutSerializer, SubscriptionPlanSerializer, UserSubscriptionSerializer, CreateSubscriptionSerializer,
    CancelSubscriptionSerializer, PaymentHistorySerializer, AccountSettingsSerializer, ChangePasswordSerializer
)
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import make_password, check_password
import secrets
from datetime import timedelta
from rest_framework.views import APIView
from rest_framework.exceptions import NotFound
from .stripe_service import StripeService
from .authentication import IsAuthenticated
import json

def home(request):
    return render(request, 'wixbuddy/home.html')

@login_required
def survey(request):
    questions = Question.objects.filter(is_active=True).order_by('order')
    return render(request, 'wixbuddy/survey.html', {'questions': questions})

def dashboard_view(request):
    return render(request, 'wixbuddy/dashboard.html')

class QuestionViewSet(viewsets.ModelViewSet):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def dashboard(request):
    """Get dashboard data for authenticated user"""
    try:
        # Fetch latest About info
        about_data = None
        try:
            about = About.objects.latest('created_at')
            about_data = AboutSerializer(about, context={'request': request}).data
        except About.DoesNotExist:
            about_data = None
        about_image_url = about_data['imageUrl'] if about_data else ''

        # Fetch dashboard images
        dashboard_images = DashboardImage.objects.order_by('order')[:3]
        card_infos = [
            {
                'header': 'AI Powered Knowledge Hub',
                'message': 'Explore AI-driven insights and resources tailored for you.',
            },
            {
                'header': 'Fitness',
                'message': 'Track your fitness journey and achieve your health goals.',
            },
            {
                'header': 'User Specific Data Hub',
                'message': 'Access your personalized data and analytics in one place.',
            },
        ]
        cards = []
        for img, card_info in zip(dashboard_images, card_infos):
            cards.append({
                'header': card_info['header'],
                'message': card_info['message'],
                'imageUrl': request.build_absolute_uri(img.image.url) if img.image else '',
            })
        return Response({'cards': cards, 'extraImageUrl': about_image_url}, status=200)
    except Exception as e:
        return Response({'error': str(e)}, status=400)

# --- AUTH VIEWS ---
@api_view(['POST'])
@permission_classes([AllowAny])
def signup(request):
    serializer = SignUpSerializer(data=request.data)
    if serializer.is_valid():
        data = serializer.validated_data
        if User.objects.filter(email=data['email']).exists():
            return Response({'error': 'Email already registered.'}, status=400)
        user = User.objects.create(
            email=data['email'],
            name=data['name'],
            family_name=data['family_name'],
            password=make_password(data['password']),
            agreed_to_policy=data['agreed_to_policy'],
            username=data['email']
        )
        # Do NOT create tokens here
        return Response({'message': 'User created successfully.', 'user': UserSerializer(user).data}, status=201)
    return Response(serializer.errors, status=400)

@api_view(['POST'])
@permission_classes([AllowAny])
def signin(request):
    serializer = SignInSerializer(data=request.data)
    if serializer.is_valid():
        data = serializer.validated_data
        try:
            user = User.objects.get(email=data['email'])
        except User.DoesNotExist:
            return Response({'error': 'Invalid credentials.'}, status=400)
        if not check_password(data['password'], user.password):
            return Response({'error': 'Invalid credentials.'}, status=400)
        access_token, refresh_token = AccessToken.create_tokens(user)
        tokens = {
            'access': access_token.token,
            'refresh': refresh_token.token,
            'expires_in': int((access_token.expires_at - timezone.now()).total_seconds())
        }
        return Response(AuthResponseSerializer({'user': user, 'tokens': tokens}).data)
    return Response(serializer.errors, status=400)

@api_view(['POST'])
@permission_classes([AllowAny])
def refresh(request):
    serializer = RefreshTokenRequestSerializer(data=request.data)
    if serializer.is_valid():
        token = serializer.validated_data['refresh']
        try:
            refresh_token = RefreshToken.objects.get(token=token, is_valid=True)
        except RefreshToken.DoesNotExist:
            return Response({'error': 'Invalid refresh token.'}, status=400)
        user = refresh_token.user
        access_token = AccessToken.objects.create(user=user)
        response = {
            'access': access_token.token,
            'expires_in': int((access_token.expires_at - timezone.now()).total_seconds())
        }
        return Response(RefreshTokenResponseSerializer(response).data)
    return Response(serializer.errors, status=400)

@api_view(['POST'])
@permission_classes([AllowAny])
def logout(request):
    token = request.headers.get('Authorization', '').replace('Bearer ', '')
    if not token:
        return Response({'error': 'No access token provided.'}, status=400)
    try:
        access_token = AccessToken.objects.get(token=token)
        access_token.is_valid = False
        access_token.save()
        return Response(LogoutResponseSerializer({'message': 'Logged out successfully.'}).data)
    except AccessToken.DoesNotExist:
        return Response({'error': 'Invalid access token.'}, status=400)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def profile(request):
    user = request.user
    return Response(UserSerializer(user).data)

@api_view(['POST'])
@permission_classes([AllowAny])
def forgot_password(request):
    serializer = ForgotPasswordSerializer(data=request.data)
    if serializer.is_valid():
        # Here you would generate and send OTP
        return Response({'message': 'OTP sent to email.'})
    return Response(serializer.errors, status=400)

@api_view(['POST'])
@permission_classes([AllowAny])
def reset_password(request):
    serializer = ResetPasswordSerializer(data=request.data)
    if serializer.is_valid():
        # Here you would verify OTP and reset password
        return Response({'message': 'Password reset successful.'})
    return Response(serializer.errors, status=400)

@api_view(['POST'])
@permission_classes([AllowAny])
def google_signin(request):
    serializer = GoogleSignInSerializer(data=request.data)
    if serializer.is_valid():
        # Here you would verify Google token and sign in user
        return Response({'message': 'Google sign in successful.'})
    return Response(serializer.errors, status=400)

@api_view(['POST'])
@permission_classes([AllowAny])
def apple_signin(request):
    serializer = AppleSignInSerializer(data=request.data)
    if serializer.is_valid():
        # Here you would verify Apple token and sign in user
        return Response({'message': 'Apple sign in successful.'})
    return Response(serializer.errors, status=400)

class AboutAPIView(APIView):
    def get(self, request):
        try:
            about = About.objects.latest('created_at')
        except About.DoesNotExist:
            raise NotFound({'detail': 'No About data found.'})
        except Exception as e:
            return Response({'detail': 'Server error.'}, status=500)
        serializer = AboutSerializer(about, context={'request': request})
        return Response({'data': serializer.data}, status=200)

# --- SUBSCRIPTION VIEWS ---
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
    serializer = CreateSubscriptionSerializer(data=request.data)
    if serializer.is_valid():
        try:
            plan = SubscriptionPlan.objects.get(
                id=serializer.validated_data['plan_id'],
                is_active=True
            )
            
            checkout_session = StripeService.create_checkout_session(
                user=request.user,
                plan=plan,
                success_url=serializer.validated_data['success_url'],
                cancel_url=serializer.validated_data['cancel_url']
            )
            
            return Response({
                'checkout_url': checkout_session.url,
                'session_id': checkout_session.id
            })
        except SubscriptionPlan.DoesNotExist:
            return Response({'error': 'Plan not found'}, status=404)
        except Exception as e:
            return Response({'error': str(e)}, status=400)
    return Response(serializer.errors, status=400)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def subscription_status(request):
    """Get current user's subscription status"""
    try:
        subscription = UserSubscription.objects.filter(
            user=request.user,
            status__in=['active', 'trialing']
        ).first()
        
        if subscription:
            serializer = UserSubscriptionSerializer(subscription)
            return Response(serializer.data)
        else:
            return Response({'message': 'No active subscription'}, status=404)
    except Exception as e:
        return Response({'error': str(e)}, status=400)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def cancel_subscription(request):
    """Cancel user's subscription"""
    try:
        serializer = CancelSubscriptionSerializer(data=request.data)
        if serializer.is_valid():
            subscription = UserSubscription.objects.filter(
                user=request.user,
                status__in=['active', 'trialing']
            ).first()
            
            if not subscription:
                return Response({'error': 'No active subscription found'}, status=404)
            
            try:
                # Cancel in Stripe
                StripeService.cancel_subscription(
                    subscription.stripe_subscription_id,
                    cancel_at_period_end=serializer.validated_data['cancel_at_period_end']
                )
                
                # Update local subscription
                subscription.cancel_at_period_end = serializer.validated_data['cancel_at_period_end']
                if not serializer.validated_data['cancel_at_period_end']:
                    subscription.status = 'canceled'
                subscription.save()
                
                return Response({'message': 'Subscription cancelled successfully'})
            except Exception as stripe_error:
                return Response({'error': f'Failed to cancel subscription: {str(stripe_error)}'}, status=400)
        else:
            return Response(serializer.errors, status=400)
    except Exception as e:
        return Response({'error': f'Internal server error: {str(e)}'}, status=500)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def payment_history(request):
    """Get user's payment history"""
    payments = PaymentHistory.objects.filter(user=request.user).order_by('-created_at')
    serializer = PaymentHistorySerializer(payments, many=True)
    return Response(serializer.data)

@api_view(['POST'])
@permission_classes([AllowAny])
def stripe_webhook(request):
    """Handle Stripe webhook events"""
    payload = request.body
    sig_header = request.META.get('HTTP_STRIPE_SIGNATURE')
    
    try:
        # Verify webhook signature (you should add your webhook secret)
        # event = stripe.Webhook.construct_event(payload, sig_header, 'whsec_your_webhook_secret')
        
        # For now, just parse the event without verification
        event = json.loads(payload)
        
        # Handle the event
        StripeService.handle_webhook_event(event)
        
        return Response({'status': 'success'})
    except ValueError as e:
        return Response({'error': 'Invalid payload'}, status=400)
    except Exception as e:
        return Response({'error': str(e)}, status=400)

# --- ACCOUNT SETTINGS VIEWS ---
@api_view(['GET', 'PUT', 'POST', 'DELETE'])
@permission_classes([IsAuthenticated])
def account_settings(request):
    """Comprehensive account settings API - handles all account operations"""
    
    if request.method == 'GET':
        """Get current user's profile information"""
        try:
            serializer = UserSerializer(request.user)
            return Response(serializer.data)
        except Exception as e:
            return Response({'error': str(e)}, status=400)
    
    elif request.method == 'PUT':
        """Update current user's profile information"""
        serializer = AccountSettingsSerializer(request.user, data=request.data, partial=True)
        if serializer.is_valid():
            try:
                serializer.save()
                return Response({
                    'message': 'Profile updated successfully',
                    'user': UserSerializer(request.user).data
                })
            except Exception as e:
                return Response({'error': str(e)}, status=400)
        return Response(serializer.errors, status=400)
    
    elif request.method == 'POST':
        """Change current user's password"""
        serializer = ChangePasswordSerializer(data=request.data)
        if serializer.is_valid():
            try:
                user = request.user
                
                # Verify current password
                if not check_password(serializer.validated_data['current_password'], user.password):
                    return Response({'error': 'Current password is incorrect'}, status=400)
                
                # Update password
                user.password = make_password(serializer.validated_data['new_password'])
                user.save()
                
                return Response({'message': 'Password changed successfully'})
            except Exception as e:
                return Response({'error': str(e)}, status=400)
        return Response(serializer.errors, status=400)
    
    elif request.method == 'DELETE':
        """Delete current user's account"""
        try:
            user = request.user
            
            # Cancel any active subscriptions
            active_subscriptions = UserSubscription.objects.filter(
                user=user, 
                status__in=['active', 'trialing']
            )
            
            for subscription in active_subscriptions:
                try:
                    StripeService.cancel_subscription(subscription.stripe_subscription_id, cancel_at_period_end=False)
                except:
                    pass  # Continue even if Stripe cancellation fails
            
            # Delete user
            user.delete()
            
            return Response({'message': 'Account deleted successfully'})
        except Exception as e:
            return Response({'error': str(e)}, status=400)
            




