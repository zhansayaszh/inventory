import secrets
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, SetPasswordForm, PasswordChangeForm
from django.contrib.auth.hashers import make_password
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from django.contrib.auth.models import User
from django import forms
from django.forms.widgets import PasswordInput, TextInput
from django.conf import settings
from django.core.mail import send_mail
from accounts.models import UserProfile
from inventory.models import CompanyModel, RoleModel
import random
import string
from django.core.exceptions import ValidationError


        
#Register User
class CreateUserForm(UserCreationForm):
    company = forms.ModelChoiceField(queryset=CompanyModel.objects.all(), required=True)
    role = forms.ModelChoiceField(queryset=RoleModel.objects.all(), required=True)
    
    def __init__(self, *args, **kwargs):
        super(CreateUserForm, self).__init__(*args, **kwargs)
        self.fields['password1'].required = False
        self.fields['password2'].required = False
        
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('submit', 'Save', css_class='btn-primary'))
        self.fields['username'].help_text = None
        self.fields['is_staff'].help_text = None
        self.fields['company'].label = 'Компания'
        self.fields['role'].label = 'Должность'
        self.fields['role'].empty_label = 'Выбрать'
        self.fields['company'].empty_label = 'Выбрать'
        
    def clean_username(self):
        username = self.cleaned_data['username']
        try:
            user = User.objects.get(username=username)
            # Check if the username has changed and if the user is not the current user being updated
            if user != self.instance:
                raise forms.ValidationError("A user with that username already exists.")
        except User.DoesNotExist:
            pass  # Username is unique
        return username
    
    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email=email).exists():
            raise ValidationError("Эта почта уже используется!")
        return email
    
    def save(self, commit=True): #CreateUserForm, self
        user = super().save(commit=False)
        user.is_active = True
        random_password = ''.join(random.choices(string.ascii_letters + string.digits, k=12))
        user.set_password(random_password)
        if commit:
            user.save()
            # Send email with the randomly generated password
            send_mail(
                'Вход в Инвентаризацию',
                'Добро пожаловать в Инвентаризацию от Bass Holding! Пожалуйста поменяйте пароль в вашем личном кабинете.'
                f'\n Логин: {user.username}\n Временный Пароль: {random_password}',
                'bass_holding@mail.ru',  # Replace with your email
                [user.email],
                fail_silently=False)
            # Create UserProfile instance and link to user
            company_name = self.cleaned_data.get('company')
            role_name = self.cleaned_data.get('role')
            UserProfile.objects.create(user=user, company=company_name, role=role_name)
        return user
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'is_staff', 'is_active', 'last_login']
        labels = {
            'username': 'Логин',
            'first_name': 'Имя*',
            'last_name': 'Фамилия*',
            'email': 'Электронная почта*',
            'is_staff': 'Модератор',
            'is_active': 'Активный',
            'last_login': 'Последний вход'
        }
    # def clean_email(self):
    #     email = self.cleaned_data.get('email')
    #     if not email:
    #         raise forms.ValidationError("This field is required.")
    #     return email
    
    # def clean(self):
    #     cleaned_data = super().clean()
        
    #     first_name = cleaned_data.get('first_name')
    #     last_name = cleaned_data.get('last_name')
    #     if not first_name:
    #         self.add_error('first_name', 'This field is required.')
    #     if not last_name:
    #         self.add_error('last_name', 'This field is required.')
        
    #     return self.cleaned_data

#Authentication     

class LoginForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(),label='Логин')
    password = forms.CharField(widget=forms.PasswordInput(),label='Пароль')

    def __init__(self, *args, **kwargs):
        super(LoginForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('submit', 'Login', css_class='btn btn-primary btn-block'))

class MyUserSetPasswordForm(SetPasswordForm):
    new_password1 = forms.CharField(max_length=50, widget=forms.PasswordInput(attrs={
        'class': 'form-control', 'placeholder': 'Новый Пароль'
    }), label="Новый Пароль")
    new_password2 = forms.CharField(max_length=50, widget=forms.PasswordInput(attrs={
        'class': 'form-control', 'placeholder': 'Потвердите новый пароль'
    }), label="Потвердите новый пароль")

class CustomPasswordChangeForm(PasswordChangeForm):
    old_password = forms.CharField(
        label="Старый пароль",  # Change the label for the old password field
        widget=forms.PasswordInput(attrs={'autocomplete': 'current-password', 'autofocus': True}),
    )
    new_password1 = forms.CharField(
        label="Новый пароль",  # Change the label for the new password field
        widget=forms.PasswordInput(attrs={'autocomplete': 'new-password'}),
        strip=False,
        help_text="Пароль не может быть меньше 8 символов.",
    )
    new_password2 = forms.CharField(
        label="Повторите новый пароль",  # Change the label for the new password confirmation field
        strip=False,
        widget=forms.PasswordInput(attrs={'autocomplete': 'new-password'}),
    )