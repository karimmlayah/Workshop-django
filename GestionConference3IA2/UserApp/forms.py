from django import forms
from .models import User
from django.contrib.auth.forms import UserCreationForm

class UserRegisterForm(UserCreationForm):
    class Meta:
        model=User
        fields=['username','first_name','last_name',
                'email','affiliation','nationality',
                'password1','password2']
        labels={
            'username':'Nom d\'utilisateur',
            'first_name':'Prénom',
            'last_name':'Nom de famille',
            'email':'Adresse e-mail',
            'affiliation':'Affiliation',
            'nationality':'Nationalité',
            'password1':'Mot de passe',
            'password2':'Confirmer le mot de passe'
        }
        widgets={
            'username':forms.TextInput(attrs={
                'class':'form-control',
                'placeholder':'Entrez votre nom d\'utilisateur'
            }),
            'first_name':forms.TextInput(attrs={
                'class':'form-control',
                'placeholder':'Entrez votre prénom'
            }),
            'last_name':forms.TextInput(attrs={
                'class':'form-control',
                'placeholder':'Entrez votre nom de famille'
            }),
            'email':forms.EmailInput(attrs={
                'class':'form-control',
                'placeholder':'Entrez votre adresse e-mail'
            }),
            'affiliation':forms.TextInput(attrs={
                'class':'form-control',
                'placeholder':'Entrez votre affiliation'
            }),
            'nationality':forms.TextInput(attrs={
                'class':'form-control',
                'placeholder':'Entrez votre nationalité'
            }),
            'password1':forms.PasswordInput(attrs={
                'class':'form-control',
                'placeholder':'Entrez votre mot de passe'
            }),
            'password2':forms.PasswordInput(attrs={
                'class':'form-control',
                'placeholder':'Confirmez votre mot de passe'
            }),
        }

