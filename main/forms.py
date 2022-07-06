from django import forms

class RegisterForm(forms.Form):
    email = forms.EmailInput()
    username = forms.CharField(max_length=100)
    password = forms.PasswordInput()