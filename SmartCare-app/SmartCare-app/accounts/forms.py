from django import forms
from .models import User

class SignupForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    class Meta:
        model = User
        fields = ['name', 'role', 'email', 'address', 'password']
        widgets = {
            'password': forms.PasswordInput(),
            'role': forms.Select()  # Ensure the role field is rendered as a dropdown
        }

class LoginForm(forms.Form):
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)

class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['name', 'email', 'role', 'address', 'password']
        # Exclude 'password' if you don't intend to update it directly via form
