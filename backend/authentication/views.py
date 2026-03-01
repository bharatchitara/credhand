import os
import json
import requests
from django.shortcuts import render, redirect
from django.contrib.auth import logout, login
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.conf import settings
from django.views.generic import TemplateView
from django.db.models import Sum, Count
from .models import CustomUser
from .utils import get_google_oauth_url, exchange_code_for_token, get_user_info
from transactions.models import Transaction
from cards.models import CreditCard


def home_view(request):
    """Home page - redirect to login or dashboard"""
    if request.user.is_authenticated:
        return redirect('dashboard')
    return render(request, 'index.html')


@login_required(login_url='authentication:login')
def dashboard_view(request):
    """Dashboard view - shows user's transactions and lending options"""
    user_transactions = Transaction.objects.filter(user=request.user).order_by('-created_at')[:10]
    available_cards = CreditCard.objects.filter(is_active=True)
    
    context = {
        'user': request.user,
        'transactions': user_transactions,
        'available_cards': available_cards,
    }
    return render(request, 'dashboard.html', context)


@login_required(login_url='authentication:login')
def card_lending_view(request):
    """Card lending page"""
    available_cards = CreditCard.objects.filter(is_active=True)
    context = {'available_cards': available_cards}
    return render(request, 'card_lending.html', context)


@login_required(login_url='authentication:login')
def transaction_history_view(request):
    """Transaction history page"""
    user_transactions = Transaction.objects.filter(user=request.user).order_by('-created_at')
    context = {'transactions': user_transactions}
    return render(request, 'transaction_history.html', context)


@login_required(login_url='authentication:login')
def payment_view(request):
    """Payment page"""
    return render(request, 'payment.html', {'user': request.user})


@login_required(login_url='authentication:login')
def payment_success_view(request):
    """Payment success page"""
    return render(request, 'payment_success.html')


@login_required(login_url='authentication:login')
def payment_failure_view(request):
    """Payment failure page"""
    return render(request, 'payment_failure.html')


def login_view(request):
    """Redirect to Google OAuth login"""
    google_auth_url = get_google_oauth_url()
    return redirect(google_auth_url)


def google_callback(request):
    """Handle Google OAuth callback"""
    code = request.GET.get('code')
    
    if not code:
        return redirect('authentication:login')
    
    try:
        # Exchange authorization code for access token
        token_data = exchange_code_for_token(code)
        access_token = token_data.get('access_token')
        
        # Get user info from Google
        user_info = get_user_info(access_token)
        
        # Create or update user
        user, created = CustomUser.objects.get_or_create(
            oauth_id=user_info['sub'],
            defaults={
                'email': user_info['email'],
                'first_name': user_info.get('given_name', ''),
                'last_name': user_info.get('family_name', ''),
                'oauth_provider': 'google',
                'username': user_info['email'],
            }
        )
        
        # Update user if already exists
        if not created:
            user.email = user_info['email']
            user.first_name = user_info.get('given_name', '')
            user.last_name = user_info.get('family_name', '')
            user.save()
        
        # Log user in
        login(request, user, backend='django.contrib.auth.backends.ModelBackend')
        
        return redirect('dashboard')  # Redirect to dashboard
    
    except Exception as e:
        print(f"Error during Google OAuth callback: {str(e)}")
        return redirect('authentication:login')


@login_required(login_url='authentication:login')
def logout_view(request):
    """Logout user"""
    logout(request)
    return redirect('home')


@login_required(login_url='authentication:login')
def profile_view(request):
    """User profile view"""
    user = request.user
    transactions = Transaction.objects.filter(user=user)

    stats = {
        'total': transactions.count(),
        'completed': transactions.filter(status='completed').count(),
        'pending': transactions.filter(status__in=['pending', 'payment_initiated']).count(),
        'total_amount': transactions.filter(status='completed').aggregate(
            s=Sum('amount'))['s'] or 0,
        'total_charges': transactions.filter(status='completed').aggregate(
            s=Sum('brokerage_amount'))['s'] or 0,
    }
    recent = transactions.order_by('-created_at')[:5]

    context = {
        'user': user,
        'stats': stats,
        'recent': recent,
    }
    return render(request, 'auth/profile.html', context)


@login_required(login_url='authentication:login')
def settings_view(request):
    """User settings view"""
    user = request.user
    success = None
    error = None

    if request.method == 'POST':
        action = request.POST.get('action')

        if action == 'update_profile':
            first_name = request.POST.get('first_name', '').strip()
            last_name = request.POST.get('last_name', '').strip()
            phone = request.POST.get('phone', '').strip()

            if first_name:
                user.first_name = first_name
            if last_name:
                user.last_name = last_name
            user.phone = phone or None
            user.save()
            success = 'Profile updated successfully.'

        elif action == 'delete_account':
            confirm = request.POST.get('confirm_delete', '').strip()
            if confirm == user.email:
                logout(request)
                user.delete()
                return redirect('home')
            else:
                error = 'Email did not match. Account not deleted.'

    return render(request, 'auth/settings.html', {
        'user': user,
        'success': success,
        'error': error,
    })
