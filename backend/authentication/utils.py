import os
import requests
from urllib.parse import urlencode
from django.conf import settings


def get_google_oauth_url():
    """Generate Google OAuth login URL"""
    params = {
        'client_id': settings.GOOGLE_OAUTH_CLIENT_ID,
        'redirect_uri': settings.GOOGLE_OAUTH_REDIRECT_URI,
        'response_type': 'code',
        'scope': 'openid email profile',
        'access_type': 'offline',
    }
    return f"https://accounts.google.com/o/oauth2/v2/auth?{urlencode(params)}"


def exchange_code_for_token(code):
    """Exchange authorization code for access token"""
    token_url = 'https://oauth2.googleapis.com/token'
    
    data = {
        'client_id': settings.GOOGLE_OAUTH_CLIENT_ID,
        'client_secret': settings.GOOGLE_OAUTH_CLIENT_SECRET,
        'code': code,
        'grant_type': 'authorization_code',
        'redirect_uri': settings.GOOGLE_OAUTH_REDIRECT_URI,
    }
    
    response = requests.post(token_url, data=data)
    return response.json()


def get_user_info(access_token):
    """Get user info from Google using access token"""
    user_info_url = 'https://openidconnect.googleapis.com/v1/userinfo'
    headers = {'Authorization': f'Bearer {access_token}'}
    
    response = requests.get(user_info_url, headers=headers)
    return response.json()
