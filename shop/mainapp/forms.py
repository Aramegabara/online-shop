from django import forms
from django.contrib.auth.forms import UserCreationForm

from .models import Order, User


class OrderForm(forms.ModelForm):

    order_date = forms.DateField(widget=forms.TextInput(attrs={'type': 'date'}))

    class Meta:
        model = Order
        fields = (
            'first_name',
            'last_name',
            'phone',
            'address',
            'buying_type',
            'order_date',
            'comment'
        )
# test

class myFormRegistration(UserCreationForm):
    password = forms.CharField(max_length=16, widget=forms.PasswordInput(attrs={'placeholder': "Password"}))
    password2 = forms.CharField(max_length=16, widget=forms.PasswordInput(attrs={'placeholder': "Confirm password"}))

    class Meta:
        model = User
        fields = (
            'first_name',
            'last_name',
            'email',
            'password',
            'password2',
            'username'
        )
        widgets = {
            'first_name': forms.TextInput(attrs={'placeholder': "First name"}),
            'last_name': forms.TextInput(attrs={'placeholder': "Last name"}),
            'email': forms.EmailInput(attrs={'placeholder': "Email"}),
            'username': forms.TextInput(attrs={'placeholder': "Username"})
        }

    def save(self, commit=True):
        user = super(myFormRegistration, self).save(commit=False)
        if commit:
            # user.is_authenticated()
            user.save()
        return user


class LoginForm(forms.ModelForm):

    password = forms.CharField(widget=forms.PasswordInput)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].label = 'Login'
        self.fields['password'].label = 'Password'

    def clean(self):
        username = self.cleaned_data['username']
        password = self.cleaned_data['password']
        if not User.objects.filter(username=username).exists():
            raise forms.ValidationError(f'User {username} is empty in system.')
        user = User.objects.filter(username=username).first()
        if user:
            if not user.check_password(password):
                raise forms.ValidationError('Incorrect password.')
        return self.cleaned_data

    class Meta:
        model = User
        fields = ['username', 'password']

