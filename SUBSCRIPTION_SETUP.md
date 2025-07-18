# Stripe Subscription System Setup

## Overview
This project now includes a complete Stripe subscription system with the following features:
- Multiple subscription plans (Basic, Pro, Premium)
- Monthly and yearly billing cycles
- Stripe Checkout integration
- Webhook handling for subscription events
- Payment history tracking

## Setup Instructions

### 1. Database Setup
The subscription models have been created and migrated. The following tables are now available:
- `SubscriptionPlan` - Stores available subscription plans
- `UserSubscription` - Tracks user subscriptions
- `PaymentHistory` - Records payment transactions

### 2. Create Stripe Products and Prices
Before using the system, you need to create products and prices in your Stripe dashboard:

1. Go to [Stripe Dashboard](https://dashboard.stripe.com/)
2. Navigate to Products > Add Product
3. Create products for each plan (Basic, Pro, Premium)
4. Add prices for each product (monthly and yearly)
5. Copy the price IDs and update them in the management command

### 3. Set Up Default Plans
Run the management command to create default subscription plans:
```bash
python manage.py setup_subscription_plans
```

**Note**: You need to update the `stripe_price_id` values in the management command with your actual Stripe price IDs.

### 4. Configure Webhooks (Optional but Recommended)
1. In Stripe Dashboard, go to Developers > Webhooks
2. Add endpoint: `https://yourdomain.com/api/webhook/stripe/`
3. Select events:
   - `customer.subscription.created`
   - `customer.subscription.updated`
   - `customer.subscription.deleted`
   - `invoice.payment_succeeded`
   - `invoice.payment_failed`
4. Copy the webhook secret and update it in the webhook handler

## API Endpoints

### Get Available Plans
```
GET /api/subscription/plans/
```
Returns all available subscription plans.

### Create Subscription
```
POST /api/subscription/create/
```
**Headers**: `Authorization: Bearer <token>`
**Body**:
```json
{
    "plan_id": 1,
    "success_url": "https://yourdomain.com/success",
    "cancel_url": "https://yourdomain.com/cancel"
}
```
Returns a Stripe Checkout URL.

### Get Subscription Status
```
GET /api/subscription/status/
```
**Headers**: `Authorization: Bearer <token>`
Returns current user's subscription status.

### Cancel Subscription
```
POST /api/subscription/cancel/
```
**Headers**: `Authorization: Bearer <token>`
**Body**:
```json
{
    "cancel_at_period_end": true
}
```

### Get Payment History
```
GET /api/subscription/payments/
```
**Headers**: `Authorization: Bearer <token>`
Returns user's payment history.

### Stripe Webhook
```
POST /api/webhook/stripe/
```
Handles Stripe webhook events (no authentication required).

## Usage Example

### Frontend Integration
```javascript
// Get available plans
const plans = await fetch('/api/subscription/plans/').then(r => r.json());

// Create subscription
const response = await fetch('/api/subscription/create/', {
    method: 'POST',
    headers: {
        'Authorization': 'Bearer ' + token,
        'Content-Type': 'application/json'
    },
    body: JSON.stringify({
        plan_id: 1,
        success_url: 'https://yourdomain.com/success',
        cancel_url: 'https://yourdomain.com/cancel'
    })
});

const { checkout_url } = await response.json();
window.location.href = checkout_url; // Redirect to Stripe Checkout
```

## Important Notes

1. **Stripe Secret Key**: The secret key is hardcoded in `stripe_service.py`. In production, use environment variables.

2. **Webhook Security**: The webhook signature verification is commented out. Enable it in production with your webhook secret.

3. **Price IDs**: Update the `stripe_price_id` values in the management command with your actual Stripe price IDs.

4. **Error Handling**: The system includes basic error handling, but you may want to add more comprehensive error handling for production.

5. **Testing**: Use Stripe's test mode for development. Switch to live mode for production.

## Security Considerations

1. Always use HTTPS in production
2. Store Stripe keys in environment variables
3. Verify webhook signatures
4. Implement proper authentication and authorization
5. Monitor webhook events for security

## Troubleshooting

1. **"No such table" errors**: Run `python manage.py migrate`
2. **Stripe errors**: Check your Stripe dashboard for error logs
3. **Webhook issues**: Verify webhook endpoint URL and events
4. **Authentication errors**: Ensure proper token authentication

## Next Steps

1. Update Stripe price IDs in the management command
2. Set up webhook endpoint in Stripe dashboard
3. Test the subscription flow
4. Implement subscription-based feature access
5. Add subscription management UI 