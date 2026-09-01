from django.shortcuts import render
from django.http import JsonResponse
from .yolo import process_stream
import json


from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
# Create your views here.
from .forms import *







def index(request):
    return render(request, 'index.html')

def process_video_view(request):
    """
    Handles video processing requests and returns a JSON response.
    """
    video_url = request.GET.get('video_url')
    if not video_url:
        return JsonResponse({'error': 'No video URL provided'}, status=400)

    try:
        process_stream(video_url)
        return JsonResponse({'message': 'Video processing started. Check the terminal for results.'})
    except Exception as e:
        return JsonResponse({'error': f'Processing failed: {str(e)}'}, status=500)
    




    


def home(request):
    return render(request, 'home.html')

def dashboard(request):
    return render(request, 'dashboard.html')

def reportincident_view(request):
    return render(request, 'reportincident.html')

def contactauthorities_view(request):
    return render(request, 'contactauthorities.html')

def guidelines_view(request):
    return render(request, 'guidelines.html')

def features_view(request):
    return render(request, 'features.html')

def howitswork_view(request):
    return render(request, 'howitswork.html')

def login_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        try:
            user = User.objects.filter(email=email).first()
            if user:
                auth_user = authenticate(request, username=user.username, password=password)
                if auth_user is not None:
                    login(request, auth_user)
                    if auth_user.is_superuser:
                        return redirect('admin-dashboard')
                    return redirect('admin-dashboard')
                else:
                    messages.error(request, 'Invalid password')
            else:
                messages.error(request, 'No account found with this email')
        except Exception as e:
            messages.error(request, 'Login error. Please try again.')
            
    return render(request, 'login.html')

@login_required(login_url='login')
def admin_dashboard(request):
    return render(request, 'admindashboard.html')

def livemonitoring_view(request):
    return render(request, 'livemonitoring.html')

def alerts_view(request):
    return render(request, 'alerts.html')

def analysis_view(request):
    return render(request, 'analysis.html')

def signup_view(request):
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            try:
                user = form.save()
                messages.success(request, 'Account created successfully! Please login.')
                return redirect('login')
            except Exception as e:
                messages.error(request, f'Error creating account: {str(e)}')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f'{field}: {error}')
    else:
        form = CreateUserForm()

    context = {'form': form}
    return render(request, 'signup.html', context)

def contact_view(request):
    return render(request, 'contact.html')

def logout_view(request):
    logout(request)
    return redirect('login')

