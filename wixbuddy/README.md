# Wix Buddy AI Assistant

## Google OAuth2 Setup Instructions

1. Go to Google Cloud Console (https://console.cloud.google.com/)
2. Create a new project or select your existing project
3. Enable the following APIs:
   - Generative Language API
   - Cloud Translation API
4. Go to "APIs & Services" → "Credentials"
5. Click "Create Credentials" → "OAuth client ID"
6. Configure the OAuth consent screen:
   - User Type: External
   - App name: Wix Buddy
   - User support email: Your email
   - Developer contact email: Your email
   - Add the following authorized domains:
     - localhost (for development)
     - Your production domain
   - Add the following scopes:
     - https://www.googleapis.com/auth/cloud-platform
7. Create the OAuth client ID:
   - Application type: Web application
   - Name: Wix Buddy Web Client
   - Authorized JavaScript origins:
     - http://localhost:8000
     - Your production domain
   - Authorized redirect URIs:
     - http://localhost:8000/oauth2callback
     - Your production domain/oauth2callback
8. Download the client configuration as JSON and save it as `credentials.json` in your project root

## Running the Application

1. Make sure you have Python 3.8+ installed
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Create and activate a virtual environment (optional but recommended)
4. Run migrations:
   ```bash
   python manage.py migrate
   ```
5. Start the development server:
   ```bash
   python manage.py runserver
   ```

## OAuth Flow

1. The application will use the OAuth2 flow to authenticate with Google
2. When making API requests, it will:
   - Check for existing credentials
   - Refresh tokens if needed
   - Request new tokens if none exist
3. The OAuth2 credentials will be stored in `token.json` in your project root
