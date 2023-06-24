from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from auth_system.models import UserRole
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
import requests


# Create your views here.

@login_required
def HomePage(request):
    user_role = UserRole.objects.get(user=request.user)
    if user_role.role == 'admin':
        return render(request, 'auth_system/admin_home.html', {'user': request.user})
    elif user_role.role == 'student':
        return render(request, 'auth_system/student_home.html', {'user': request.user})
    else:
        return HttpResponse('Unknown user role')

from django.core.exceptions import ValidationError

def Register(request):
    if request.method == 'POST':
        fname = request.POST.get('fname')
        lname = request.POST.get('sname')
        name = request.POST.get('uname')
        email = request.POST.get('email')
        password = request.POST.get('pass')
        role = request.POST.get('role')

        # Check if a user with the same email already exists
        if User.objects.filter(email=email).exists():
            raise ValidationError('A user with this email already exists')

        # Create a new user
        new_user = User.objects.create_user(name, email, password)
        new_user.first_name = fname
        new_user.last_name = lname
        new_user.save()

        user_role = UserRole(user=new_user, role=role)
        user_role.save()

        return redirect('login-page')

    return render(request, 'auth_system/register.html', {})


def Login(request):
    if request.method == 'POST':
        name = request.POST.get('uname')
        password = request.POST.get('pass')

        user = authenticate(request, username=name, password=password)
        if user is not None:
            login(request, user)
            return redirect('home-page')
        else:
            return HttpResponse('Error, user does not exist')


    return render(request, 'auth_system/login.html', {})

def logoutuser(request):
    logout(request)
    return redirect('login-page')

def test(request):
    return render(request, 'auth_system/test.html', {})


def profile(request):
    if request.method == 'POST':
        url = request.POST.get('url')
        api_endpoint = 'https://nubela.co/proxycurl/api/v2/linkedin'
        linkedin_profile_url = url
        api_key = 'Jy67dN9i8zGDohizQHXAqQ'
        headers = {'Authorization': 'Bearer ' + api_key}

        response = requests.get(api_endpoint,
                                params={'url': linkedin_profile_url, 'skills': 'include'},
                                headers=headers)
        profile_data = response.json()
        profile_data
        return render(request, 'auth_system/profile.html', {'name':profile_data['full_name'],'occupation':profile_data['occupation'],'headline':profile_data['headline'],'summary':profile_data['summary']})
    return render(request, 'auth_system/profile.html', {})