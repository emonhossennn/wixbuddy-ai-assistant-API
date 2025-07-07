# Authentication Troubleshooting Guide

## Problem: "You do not have permission to perform this action."

This error occurs when the authentication system isn't working properly. Here's how to fix it:

## ✅ **Solution Implemented**

I've fixed the authentication issue by:

1. **Created Custom Authentication Class** (`wixbuddy/authentication.py`)
2. **Updated REST Framework Settings** to use the custom authentication
3. **Updated Views** to use the custom permission classes
4. **Simplified Dashboard View** to use automatic authentication

## 🔧 **How to Test**

### 1. Make sure the server is running:
```bash
python manage.py runserver
```

### 2. Test the authentication flow:

#### Step 1: Sign Up
```bash
curl -X POST http://localhost:8000/api/auth/signup/ \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@example.com",
    "name": "Test",
    "family_name": "User",
    "password": "testpassword123",
    "agreed_to_policy": true
  }'
```

#### Step 2: Sign In (Get Token)
```bash
curl -X POST http://localhost:8000/api/auth/signin/ \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@example.com",
    "password": "testpassword123"
  }'
```

#### Step 3: Use Token for Authenticated Endpoints
```bash
curl -X GET http://localhost:8000/api/account-settings/ \
  -H "Authorization: Bearer YOUR_TOKEN_HERE" \
  -H "Content-Type: application/json"
```

### 3. Use the Test Script:
```bash
python test_auth.py
```

## 🔍 **Common Issues & Solutions**

### Issue 1: "No authentication credentials provided"
**Solution:** Make sure you're including the Authorization header:
```
Authorization: Bearer your_token_here
```

### Issue 2: "Invalid or expired token"
**Solution:** 
- Get a fresh token by signing in again
- Check if the token format is correct: `Bearer token_value`

### Issue 3: "Access token has expired"
**Solution:** 
- Sign in again to get a new token
- Tokens expire after 1 hour

### Issue 4: "User not found"
**Solution:** 
- Make sure the user exists (sign up first)
- Check if the email is correct

## 📋 **API Endpoints That Require Authentication**

- `GET /api/dashboard/` - Dashboard data
- `GET /api/account-settings/` - Get profile
- `PUT /api/account-settings/` - Update profile
- `POST /api/account-settings/` - Change password
- `DELETE /api/account-settings/` - Delete account
- `GET /api/subscription/status/` - Subscription status
- `POST /api/subscription/create/` - Create subscription
- `POST /api/subscription/cancel/` - Cancel subscription
- `GET /api/subscription/payments/` - Payment history

## 📋 **API Endpoints That Don't Require Authentication**

- `POST /api/auth/signup/` - User registration
- `POST /api/auth/signin/` - User login
- `POST /api/auth/refresh/` - Refresh token
- `POST /api/auth/logout/` - User logout
- `GET /api/subscription/plans/` - Get subscription plans
- `POST /api/webhook/stripe/` - Stripe webhook
- `GET /api/about` - About information

## 🔐 **Token Format**

Always use this format in the Authorization header:
```
Authorization: Bearer your_access_token_here
```

## 🧪 **Testing with Postman/Insomnia**

1. **Sign Up/Sign In** to get a token
2. **Copy the access token** from the response
3. **Add Authorization header** to subsequent requests:
   - Key: `Authorization`
   - Value: `Bearer your_token_here`

## 🐛 **Debug Mode**

If you're still having issues, you can temporarily enable debug mode by adding this to your view:

```python
@api_view(['GET'])
@permission_classes([AllowAny])  # Temporarily allow all
def debug_auth(request):
    print(f"User: {request.user}")
    print(f"Headers: {request.headers}")
    return Response({"message": "Debug info"})
```

## 📞 **Still Having Issues?**

1. Check the Django server logs for error messages
2. Verify the token is being sent correctly
3. Make sure the user exists in the database
4. Check if the token hasn't expired
5. Ensure you're using the correct API endpoints

The authentication system should now work properly! 🎉 