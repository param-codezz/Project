from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import redirect, render, HttpResponse
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login

# Create your views here.
def index(request):
    return render(request, 'index.html')

@csrf_exempt
def signin(request):
    if request.method == "POST":
        email = request.POST['user-email']
        password = request.POST['user-password']
        user = authenticate(username= email, password= password)
        if user is not None:
            login(request, user)
            name = request.user.first_name
            return redirect('/profile')
        
        else:
            messages.error(request, "Bad Credentials")
            return redirect('home')


    return render(request, 'login.html')

@csrf_exempt
def signup(request):
    if request.method == "POST":
        name = request.POST['user-name']
        email = request.POST['user-email']
        password1 = request.POST['user-password']
        passsword2 = request.POST['user-password2']
        if User.objects.filter(email = email):
            messages.error(request, "Already registered")
            redirect('/home')
        if password1 != passsword2:
            messages.error(request, "Password doesn't match")

        myuser = User.objects.create_user(email, email, password1)
        myuser.first_name = name
        myuser.save()
        messages.success(request, "Account successfully created")

        return redirect('/login')
    return render(request, 'signup.html')

def find(request):
    return render(request, 'find.html')

def terms(request):
    return render(request, 'terms.html')

def ourBrands(request):
    return HttpResponse('This is our brands page')

def aboutUs(request):
    return HttpResponse('This is about us page')

def home(request):
    return redirect('/')

def profile(request):
    name = request.user.first_name
    return render(request, 'profile.html', {'username': name})