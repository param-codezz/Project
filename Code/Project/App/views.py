from django.shortcuts import render, HttpResponse

# Create your views here.
def index(request):
    return render(request, 'index.html')

def login(request):
    return render(request, 'login.html')

def find(request):
    return HttpResponse('This is find page')

def vacation(request):
    return HttpResponse('This is vacation page')

def ourBrands(request):
    return HttpResponse('This is our brands page')

def aboutUs(request):
    return HttpResponse('This is about us page')

def profile(request):
    return HttpResponse('This is profile page')