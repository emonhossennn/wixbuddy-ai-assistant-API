import stripe
import os
from django.conf import settings
from django.utils import timezone
from .models import User, SubscriptionPlan, UserSubscription, PaymentHistory

# Initialize Stripe with your secret key from environment variables
stripe.api_key = os.getenv('STRIPE_SECRET_KEY', 'sk_test_your_stripe_secret_key_here')

class StripeService:
    @staticmethod
    def create_customer(user):
        """Create a Stripe customer for the user"""
        try:
            customer = stripe.Customer.create(
                email=user.email,
                name=f"{user.name} {user.family_name}",
                metadata={
                    'user_id': user.id,
                    'email': user.email
                }
            )
            return customer
        except stripe.error.StripeError as e:
            raise Exception(f"Failed to create Stripe customer: {str(e)}")

    @staticmethod
    def create_checkout_session(user, plan, success_url, cancel_url):
        """Create a Stripe checkout session for subscription"""
        try:
            # Get or create Stripe customer
            customer = StripeService.get_or_create_customer(user)
            
            checkout_session = stripe.checkout.Session.create(
                customer=customer.id,
                payment_method_types=['card'],
                line_items=[{
                    'price': plan.stripe_price_id,
                    'quantity': 1,
                }],
                mode='subscription',
                success_url=success_url,
                cancel_url=cancel_url,
                metadata={
                    'user_id': user.id,
                    'plan_id': plan.id
                }
            )
            return checkout_session
        except stripe.error.StripeError as e:
            raise Exception(f"Failed to create checkout session: {str(e)}")

    @staticmethod
    def get_or_create_customer(user):
        """Get existing Stripe customer or create new one"""
        try:
            # Check if user already has a subscription with customer ID
            existing_subscription = UserSubscription.objects.filter(user=user).first()
            if existing_subscription:
                customer = stripe.Customer.retrieve(existing_subscription.stripe_customer_id)
                return customer
            
            # Create new customer
            return StripeService.create_customer(user)
        except stripe.error.StripeError as e:
            raise Exception(f"Failed to get/create customer: {str(e)}")

    @staticmethod
    def cancel_subscription(subscription_id, cancel_at_period_end=True):
        """Cancel a Stripe subscription"""
        try:
            if cancel_at_period_end:
                subscription = stripe.Subscription.modify(
                    subscription_id,
                    cancel_at_period_end=True
                )
            else:
                subscription = stripe.Subscription.cancel(subscription_id)
            
            return subscription
        except stripe.error.StripeError as e:
            raise Exception(f"Failed to cancel subscription: {str(e)}")

    @staticmethod
    def get_subscription(subscription_id):
        """Get subscription details from Stripe"""
        try:
            return stripe.Subscription.retrieve(subscription_id)
        except stripe.error.StripeError as e:
            raise Exception(f"Failed to get subscription: {str(e)}")

    @staticmethod
    def handle_webhook_event(event):
        """Handle Stripe webhook events"""
        try:
            if event['type'] == 'customer.subscription.created':
                StripeService.handle_subscription_created(event['data']['object'])
            elif event['type'] == 'customer.subscription.updated':
                StripeService.handle_subscription_updated(event['data']['object'])
            elif event['type'] == 'customer.subscription.deleted':
                StripeService.handle_subscription_deleted(event['data']['object'])
            elif event['type'] == 'invoice.payment_succeeded':
                StripeService.handle_payment_succeeded(event['data']['object'])
            elif event['type'] == 'invoice.payment_failed':
                StripeService.handle_payment_failed(event['data']['object'])
        except Exception as e:
            raise Exception(f"Failed to handle webhook event: {str(e)}")

    @staticmethod
    def handle_subscription_created(subscription_data):
        """Handle subscription created event"""
        try:
            user_id = subscription_data['metadata'].get('user_id')
            plan_id = subscription_data['metadata'].get('plan_id')
            
            if not user_id or not plan_id:
                return
            
            user = User.objects.get(id=user_id)
            plan = SubscriptionPlan.objects.get(id=plan_id)
            
            UserSubscription.objects.create(
                user=user,
                plan=plan,
                stripe_subscription_id=subscription_data['id'],
                stripe_customer_id=subscription_data['customer'],
                status=subscription_data['status'],
                current_period_start=timezone.datetime.fromtimestamp(
                    subscription_data['current_period_start'], tz=timezone.utc
                ),
                current_period_end=timezone.datetime.fromtimestamp(
                    subscription_data['current_period_end'], tz=timezone.utc
                )
            )
        except (User.DoesNotExist, SubscriptionPlan.DoesNotExist):
            pass

    @staticmethod
    def handle_subscription_updated(subscription_data):
        """Handle subscription updated event"""
        try:
            subscription = UserSubscription.objects.get(
                stripe_subscription_id=subscription_data['id']
            )
            
            subscription.status = subscription_data['status']
            subscription.current_period_start = timezone.datetime.fromtimestamp(
                subscription_data['current_period_start'], tz=timezone.utc
            )
            subscription.current_period_end = timezone.datetime.fromtimestamp(
                subscription_data['current_period_end'], tz=timezone.utc
            )
            subscription.cancel_at_period_end = subscription_data['cancel_at_period_end']
            subscription.save()
        except UserSubscription.DoesNotExist:
            pass

    @staticmethod
    def handle_subscription_deleted(subscription_data):
        """Handle subscription deleted event"""
        try:
            subscription = UserSubscription.objects.get(
                stripe_subscription_id=subscription_data['id']
            )
            subscription.status = 'canceled'
            subscription.save()
        except UserSubscription.DoesNotExist:
            pass

    @staticmethod
    def handle_payment_succeeded(invoice_data):
        """Handle payment succeeded event"""
        try:
            subscription = UserSubscription.objects.get(
                stripe_subscription_id=invoice_data['subscription']
            )
            
            PaymentHistory.objects.create(
                user=subscription.user,
                subscription=subscription,
                stripe_payment_intent_id=invoice_data['payment_intent'],
                amount=invoice_data['amount_paid'] / 100,  # Convert from cents
                currency=invoice_data['currency'],
                status='succeeded'
            )
        except UserSubscription.DoesNotExist:
            pass

    @staticmethod
    def handle_payment_failed(invoice_data):
        """Handle payment failed event"""
        try:
            subscription = UserSubscription.objects.get(
                stripe_subscription_id=invoice_data['subscription']
            )
            
            PaymentHistory.objects.create(
                user=subscription.user,
                subscription=subscription,
                stripe_payment_intent_id=invoice_data['payment_intent'],
                amount=invoice_data['amount_due'] / 100,  # Convert from cents
                currency=invoice_data['currency'],
                status='failed'
            )
        except UserSubscription.DoesNotExist:
            pass 