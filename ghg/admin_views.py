from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.contrib import messages
from django.utils.translation import gettext as _
from django.urls import reverse

def custom_admin_login(request):
    if request.user.is_authenticated:
        return redirect('ghg:index')
    
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            next_url = request.POST.get('next')
            if next_url:
                return redirect(next_url)
            return redirect('ghg:index')
        else:
            messages.error(request, _('Please enter the correct username and password.'))
    
    return render(request, 'admin/login.html', {
        'next': request.GET.get('next', '')
    })

def custom_logout(request):
    logout(request)
    return redirect('ghg:admin_login')
