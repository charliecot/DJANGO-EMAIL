from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

class RegistrationForm(UserCreationForm):
    email= forms.EmailField(required=True)
    class Meta:
        model= User
        fields =['username', 'email', 'password1','password2']
        
    def clean_email(self):
        email=self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise ValidationError('an account with email already exits')
        
        return email
            
        

