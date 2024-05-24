from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from django.core.mail import send_mail
# from .forms import RegisterUserForm

# Create your views here.
def login_user(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username = username, password = password)
        if user is not None:
            login(request, user)
            messages.success(request, 'You have successfully logged in')

            return redirect('home')
        else:
            messages.error(request, 'There was an Error, Try Again!')
            return redirect('login')

  
    return render(request, 'login.html', {})   

def logout_user(request):
    logout(request)
    messages.success(request, 'You have successfully logged out')
    return redirect('home')

def register_user(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            user = authenticate(username = username, password = password)
            login(request, user)
            messages.success(request, 'You have successfully Registered')

            if request.method == 'POST' : 
                message = 'Email Registration Successful'
                email = request.POST[request.user.email]
                name = request.POST[request.user]
                send_mail(name, message, 'settings.EMAIL_HOST_USER', [email], fail_silently=False )
                return render('send_email.html')
            return redirect('home')
    else:
        form = UserCreationForm()

    return render(request, 'register.html', {'form' : form})
