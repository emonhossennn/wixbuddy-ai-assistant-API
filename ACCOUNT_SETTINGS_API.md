# Account Settings API Documentation

## Overview
The Account Settings API provides a comprehensive interface for managing user account information, including profile details, password changes, and account deletion. All operations are handled through a single endpoint using different HTTP methods.

## API Endpoint
```
/api/account-settings/
```

## Authentication
All requests require authentication using Bearer token:
```
Authorization: Bearer <your_access_token>
```

## Available Operations

### 1. Get Profile Information
**Method:** `GET`
**URL:** `/api/account-settings/`

**Response:**
```json
{
    "id": 1,
    "email": "user@example.com",
    "name": "John",
    "family_name": "Doe",
    "is_email_verified": true,
    "job_title": "Software Engineer",
    "current_company": "Tech Corp"
}
```

### 2. Update Profile Information
**Method:** `PUT`
**URL:** `/api/account-settings/`

**Request Body:**
```json
{
    "name": "John",
    "family_name": "Smith",
    "job_title": "Senior Developer",
    "current_company": "New Tech Corp"
}
```

**Note:** Email cannot be updated through this endpoint for security reasons.

**Response:**
```json
{
    "message": "Profile updated successfully",
    "user": {
        "id": 1,
        "email": "user@example.com",
        "name": "John",
        "family_name": "Smith",
        "is_email_verified": true,
        "job_title": "Senior Developer",
        "current_company": "New Tech Corp"
    }
}
```

### 3. Change Password
**Method:** `POST`
**URL:** `/api/account-settings/`

**Request Body:**
```json
{
    "current_password": "oldpassword123",
    "new_password": "newpassword123",
    "confirm_password": "newpassword123"
}
```

**Validation Rules:**
- New password must be at least 8 characters long
- New password and confirm password must match
- Current password must be correct

**Response:**
```json
{
    "message": "Password changed successfully"
}
```

### 4. Delete Account
**Method:** `DELETE`
**URL:** `/api/account-settings/`

**Response:**
```json
{
    "message": "Account deleted successfully"
}
```

**Note:** This will:
- Cancel any active subscriptions
- Permanently delete the user account
- This action cannot be undone

## Error Responses

### Validation Errors
```json
{
    "error": "Current password is incorrect"
}
```

### Server Errors
```json
{
    "error": "An error occurred while processing your request"
}
```

## Usage Examples

### JavaScript/Fetch API
```javascript
const API_BASE = 'https://yourdomain.com/api';
const token = 'your_access_token';

// Get profile
const getProfile = async () => {
    const response = await fetch(`${API_BASE}/account-settings/`, {
        method: 'GET',
        headers: {
            'Authorization': `Bearer ${token}`,
            'Content-Type': 'application/json'
        }
    });
    return response.json();
};

// Update profile
const updateProfile = async (profileData) => {
    const response = await fetch(`${API_BASE}/account-settings/`, {
        method: 'PUT',
        headers: {
            'Authorization': `Bearer ${token}`,
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(profileData)
    });
    return response.json();
};

// Change password
const changePassword = async (passwordData) => {
    const response = await fetch(`${API_BASE}/account-settings/`, {
        method: 'POST',
        headers: {
            'Authorization': `Bearer ${token}`,
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(passwordData)
    });
    return response.json();
};

// Delete account
const deleteAccount = async () => {
    const response = await fetch(`${API_BASE}/account-settings/`, {
        method: 'DELETE',
        headers: {
            'Authorization': `Bearer ${token}`,
            'Content-Type': 'application/json'
        }
    });
    return response.json();
};
```

### cURL Examples

#### Get Profile
```bash
curl -X GET \
  https://yourdomain.com/api/account-settings/ \
  -H 'Authorization: Bearer your_access_token'
```

#### Update Profile
```bash
curl -X PUT \
  https://yourdomain.com/api/account-settings/ \
  -H 'Authorization: Bearer your_access_token' \
  -H 'Content-Type: application/json' \
  -d '{
    "name": "John",
    "family_name": "Smith",
    "job_title": "Senior Developer",
    "current_company": "New Tech Corp"
  }'
```

#### Change Password
```bash
curl -X POST \
  https://yourdomain.com/api/account-settings/ \
  -H 'Authorization: Bearer your_access_token' \
  -H 'Content-Type: application/json' \
  -d '{
    "current_password": "oldpassword123",
    "new_password": "newpassword123",
    "confirm_password": "newpassword123"
  }'
```

#### Delete Account
```bash
curl -X DELETE \
  https://yourdomain.com/api/account-settings/ \
  -H 'Authorization: Bearer your_access_token'
```

## Security Considerations

1. **Password Security:**
   - Passwords are hashed using Django's secure hashing
   - Current password verification required for changes
   - Minimum password length enforced

2. **Email Protection:**
   - Email address cannot be changed via this endpoint
   - Email verification status is read-only

3. **Account Deletion:**
   - Irreversible action
   - Automatically cancels active subscriptions
   - Requires authentication

4. **Data Validation:**
   - All input data is validated
   - SQL injection protection through Django ORM
   - XSS protection through proper serialization

## Field Descriptions

| Field | Type | Description | Editable |
|-------|------|-------------|----------|
| id | Integer | User ID | No |
| email | String | User email address | No |
| name | String | User's name | Yes |
| family_name | String | User's family name | Yes |
| is_email_verified | Boolean | Email verification status | No |
| job_title | String | User's job title | Yes |
| current_company | String | User's current company | Yes |

## Status Codes

- `200 OK` - Request successful
- `400 Bad Request` - Validation error or invalid data
- `401 Unauthorized` - Authentication required or invalid token
- `500 Internal Server Error` - Server error

## Notes

- All timestamps are in UTC
- Profile updates are partial - only send fields you want to update
- Password changes require current password verification
- Account deletion is permanent and cannot be undone
- Email address changes are not supported through this endpoint for security reasons 