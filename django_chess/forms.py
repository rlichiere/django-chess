from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from django.core.validators import RegexValidator
from django.forms.widgets import PasswordInput, EmailInput


class AuthForm(AuthenticationForm):
    username = forms.CharField()
    password = forms.CharField(widget=PasswordInput())


class RegistrationForm(forms.Form):
    username = forms.CharField(label='Player name', max_length=200,
                               validators=[RegexValidator(regex='^[a-zA-Z0-9_-]*$', message='Invalid Username')])
    email = forms.CharField(widget=EmailInput())
    password = forms.CharField(widget=PasswordInput())

    def __init__(self, *args, **kwargs):
        super(RegistrationForm, self).__init__(*args, **kwargs)

    def execute(self):
        try:
            username = self.cleaned_data['username']
            email = self.cleaned_data['email']
            password = self.cleaned_data['password']

            user = User.objects.create_user(username, email, password)
            user.save()
        except Exception as e:
            return False, 'User creation error : %s' % e.message
        return True, 'User created'
