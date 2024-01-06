# from .models import Student


from django import forms
from django.contrib.auth.forms import UserCreationForm, SetPasswordForm
from .models import *
from django.contrib.auth.forms import AuthenticationForm


class UserRegisterForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ('email', 'image', 'first_name', 'last_name', 'phone_number', 'password1', 'password2')


class LoginForm(AuthenticationForm):
    class Meta:
        model = CustomUser
        fields = ('email', 'password1')

class PasswordSetForm(SetPasswordForm):
    new_password1 = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "class": "text-box form-control",
                "placeholder": "Password",
                "type": 'password',
            }
        )
    )
    new_password2 = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "class": "text-box form-control",
                "placeholder": "Confirm new password",
                "type": 'password',
            }
        )
    )

    class Meta:
        fields = ('new_password1', 'new_password2')


        
        
class BlogForm(forms.ModelForm):
    class Meta:
        model = Blog
        fields = ['image', 'title', 'description']


class BlogCommentFrom(forms.ModelForm):
    class Meta:
        model = BlogComment
        fields = ['user', 'blog', 'comment']
        

