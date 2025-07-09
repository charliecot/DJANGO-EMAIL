from django.shortcuts import render,redirect
from .form import RegistrationForm
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from emailproject.token import acount_activation_token
from django.core.mail import EmailMessage
from django.contrib import messages
from django.contrib.auth import get_user_model, login
from django.contrib.auth.models import User
from django.urls import reverse

# Create your views here.


def index(request):
    display_message= messages.get_messages(request)
    context={
        "messages":display_message
    }
    
    return render(request, 'Register/index.html', context)


def UserRegistration(request):
    form = RegistrationForm()
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active=False
            user.save()

            current_site = get_current_site(request)
            email_subjects = 'Activation account'
            massage = render_to_string("AccountActivation/EmailActivate.html",{
                "user": user,
                "domain": current_site.domain,
                'uid':urlsafe_base64_encode(force_bytes(user.pk)),
                "token":acount_activation_token.make_token(user)
                
            })
            
            
            to_email = form.cleaned_data.get('email')
            email = EmailMessage(email_subjects,massage,to=[to_email])
            email.send()
            messages.success(request,'please check your email to complete the registration') 
            return redirect('index')
    context={
            "form":form
        }
    return render(request,"Register/register.html", context)
    
                   
def activate(request,uidb64, token ):
    user= get_user_model()
    
    try:
        uid= force_str(urlsafe_base64_decode(uidb64))
        user=User.objects.get(pk=uid)
    except (TypeError,ValueError,OverflowError,user.DoesNotExist):
        user=None
        
    if user is not None and acount_activation_token.check_token(user,token):
        user.is_active=True
        user.save()
        login(request, user)
        
        messages.success(request,"your account has been successfully activated!")
        return redirect(reverse('login'))
    else :
        messages.error(request,"activation link is invalid or has expired")
        return redirect("index")
                          