from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import os
import json
from django.conf import settings
import requests
from datetime import datetime, timedelta

class GoogleOAuth2:
    def __init__(self):
        self.SCOPES = ['https://www.googleapis.com/auth/cloud-platform']
        self.CREDENTIALS_FILE = os.path.join(settings.BASE_DIR, 'credentials.json')
        self.TOKEN_FILE = os.path.join(settings.BASE_DIR, 'token.json')

    def get_credentials(self):
        """Get valid user credentials from storage.
        If nothing has been stored, or if the stored credentials are invalid,
        the OAuth 2.0 flow is completed to obtain the new credentials.
        """
        creds = None
        
        # Load credentials from token file if it exists
        if os.path.exists(self.TOKEN_FILE):
            try:
                creds = Credentials.from_authorized_user_file(self.TOKEN_FILE, self.SCOPES)
            except Exception as e:
                print(f"Error loading credentials: {e}")
                os.remove(self.TOKEN_FILE)

        # If credentials are not valid, run the OAuth flow
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                try:
                    creds.refresh(Request())
                except Exception as e:
                    print(f"Error refreshing token: {e}")
                    os.remove(self.TOKEN_FILE)
                    creds = None

            if not creds:
                # Load client secrets from credentials file
                if not os.path.exists(self.CREDENTIALS_FILE):
                    raise Exception("Credentials file not found. Please download from Google Cloud Console.")

                flow = InstalledAppFlow.from_client_secrets_file(
                    self.CREDENTIALS_FILE, self.SCOPES)
                creds = flow.run_local_server(port=0)

            # Save the credentials for the next run
            with open(self.TOKEN_FILE, 'w') as token:
                token.write(creds.to_json())

        return creds

    def get_access_token(self):
        """Get the current access token"""
        creds = self.get_credentials()
        return creds.token if creds else None

    def is_authenticated(self):
        """Check if we have valid credentials"""
        creds = self.get_credentials()
        return creds is not None and creds.valid

    def get_authorization_url(self):
        """Get the authorization URL for user to complete OAuth flow"""
        flow = InstalledAppFlow.from_client_secrets_file(
            self.CREDENTIALS_FILE, self.SCOPES)
        return flow.authorization_url(access_type='offline', prompt='consent')[0]

    def complete_authorization(self, code):
        """Complete the OAuth flow with authorization code"""
        flow = InstalledAppFlow.from_client_secrets_file(
            self.CREDENTIALS_FILE, self.SCOPES)
        creds = flow.fetch_token(code=code)
        with open(self.TOKEN_FILE, 'w') as token:
            token.write(creds.to_json())
        return creds

    def make_authenticated_request(self, url, method='GET', data=None):
        """Make an authenticated request to Google's API"""
        creds = self.get_credentials()
        if not creds:
            raise Exception("Not authenticated")

        headers = {
            'Authorization': f'Bearer {creds.token}',
            'Content-Type': 'application/json'
        }

        if method == 'GET':
            response = requests.get(url, headers=headers)
        elif method == 'POST':
            response = requests.post(url, headers=headers, json=data)
        else:
            raise ValueError(f"Unsupported method: {method}")

        return response
