from .models import Books
from django.forms import ModelForm, TextInput, NumberInput
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django import forms


class BooksForm(ModelForm):
    class Meta:
        model = Books
        fields = ['name', 'author', 'price']

        widgets = {
            'name': TextInput(attrs={
                'class': 'form-control',
                'placeholder': "Название книги"
            }),
            'author': TextInput(attrs={
                'class': 'form-control',
                'placeholder': "Автор книги"
            }),
            'price': NumberInput(attrs={
                'class': 'form-control',
                'placeholder': "Цена книги",
            })
        }


class UserRegisterForm(UserCreationForm, ModelForm):
    username = forms.CharField(label='Никнейм', widget=forms.TextInput(attrs={'class': 'form-control', 'id': 'usernameField'},))
    password1 = forms.CharField(min_length=8, label='Пароль', widget=forms.PasswordInput(attrs={'class': 'form-control', 'id': 'password1Field'},))
    password2 = forms.CharField(min_length=8, label='Подтверждение пароля', widget=forms.PasswordInput(attrs={'class': 'form-control', 'id': 'password2Field'},))
    email = forms.EmailField(label='Email', widget=forms.EmailInput(attrs={'class': 'form-control', 'id': 'emailField'},))
    first_name = forms.CharField(label='Имя', widget=forms.TextInput(attrs={'class': 'form-control', 'id': 'firstnameField'},))

    class Meta:
        model = User
        fields = ('username', 'password1', 'password2', 'email', 'first_name')

    def clean(self):
        cleaned_data = super().clean()
        if User.objects.filter(email=cleaned_data.get('email')).exists():
            self.add_error('email', 'Пользователь с данной почтой уже зарегестрирован')
        return cleaned_data


class UserLoginForm(AuthenticationForm):
    username = forms.CharField(label='Никнейм', widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput(attrs={'class': 'form-control'}))


class EmailChangeForm(forms.ModelForm):
    email = forms.EmailField(label='Email', widget=forms.EmailInput(attrs={'class': 'form-control'},))

    class Meta:
        model = User
        fields = ('email', )

    def clean(self):
        cleaned_data = super().clean()
        if User.objects.filter(email=cleaned_data.get('email')).exists():
            self.add_error('email', 'Пользователь с данной почтой уже зарегестрирован')
        return cleaned_data


class FirstNameChangeForm(forms.ModelForm):
    first_name = forms.CharField(label='Имя', widget=forms.TextInput(attrs={'class': 'form-control'},))

    class Meta:
        model = User
        fields = ('first_name', )
