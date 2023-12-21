from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import redirect, render, HttpResponse
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.core.mail import send_mail, EmailMessage
from Project_GRI import settings
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from . tokens import generate_token
from django.urls import reverse

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

        myuser = User.objects.create_user(username= email, email=email, password= password1)
        myuser.first_name = name
        myuser.is_active = False
        myuser.save()
        messages.success(request, "Account successfully created")

        subject = "Welcome to Gotham Regency Inn"
        message = f"Hello {myuser.first_name},\n\nWe thank you for becoming a member of GRI. We provide experience for handcrafted luxury.\nPlease activate your account from the next mail.\n\nThank You,\nGotham Regency Inn"
        from_email = settings.EMAIL_HOST_USER
        to_mail = [myuser.email]
        send_mail(subject, message, from_email, recipient_list=to_mail, fail_silently=False)

        #confirmation mail
        current_site = get_current_site(request)
        email_subject = "Confirm Email for GRI"
        uid = urlsafe_base64_encode(force_bytes(myuser.pk))
        token = generate_token.make_token(myuser)
        activation_url = reverse('activate', kwargs={'uidb64': uid, 'token': token})
        email_message = render_to_string('email_confirmation.html', 
        {
            'name': myuser.first_name,
            'domain': current_site.domain,
            'activation_url': activation_url,
        })
        email = EmailMessage(
            email_subject,
            email_message,
            settings.EMAIL_HOST_USER,
            [myuser.email],
        )
        email.send(fail_silently= True)
        return redirect('/login')
    return render(request, 'signup.html')

def activate(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        myuser = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        myuser = None
    
    if myuser is not None and generate_token.check_token(myuser, token):
        myuser.is_active = True
        myuser.save()
        login(request, myuser) 
        messages.success(request, "Email Confirmation successfull")
        return redirect("/home")
    else:
        messages.error(request, "Email not confirmed")
        return redirect('/home')
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
    username = request.user.username
    user_membership = 'Gold'
    if request.method == "POST":
        button = request.POST['handle_button']
        if button == "gold":
            user_membership = 'Gold'
            messages.success(request, f"Upgraded membership to {user_membership}")
        elif button == "goldpro":
            user_membership = 'GoldPro'
            messages.success(request, f"Upgraded membership to {user_membership}")
        elif button == "renew":
            messages.success(request, f"Renewed membership. Current membership status {user_membership}")
        elif button == "logout":
            logout(request)
            messages.warning(request, "Account Logged Out")
            return redirect("/home")
        elif button == "delete":
            User.objects.get(username= username).delete()
            messages.warning(request, "Account Deleted")
            return redirect("/home")
    return render(request, 'profile.html', {'username': name, 'membership': user_membership})