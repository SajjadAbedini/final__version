from django import forms
from captcha.fields import CaptchaField
from django.contrib.auth.models import User
from django.contrib.auth import (
    authenticate,
    login,
    logout,
    get_user_model
    )
from django.db import models
from datetime import datetime

user = get_user_model()


class UserLoginFormcaptcha(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={'placeholder': '  نام کاربری '}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': '  رمز عبور '}))
    captcha = CaptchaField(error_messages={'invalid': 'متن تصویر نادرست وارد شده است'})

    def clean(self, *args, **kwargs):
        username = self.cleaned_data.get("username")
        password = self.cleaned_data.get("password")
        captcha = self.cleaned_data.get("captcha")
        if username and password:
            user1 = authenticate(username=username, password=password, captcha=captcha)
            if not user1:
                print("1 error captcha")
                raise forms.ValidationError("اطلاعات وارد شده صحیح نمیباشد")
        return super(UserLoginFormcaptcha, self).clean(*args, **kwargs)

class UserLoginForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={'placeholder': '  نام کاربری '}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': '  رمز عبور '}))

    def clean(self, *args, **kwargs):
        username = self.cleaned_data.get("username")
        password = self.cleaned_data.get("password")
        if username and password:
            user = authenticate(username=username, password=password)
            if not user:
                print("1 error")
                raise forms.ValidationError("نام کاربری یا گذرواژه اشتباه است")
        return super(UserLoginForm, self).clean(*args, **kwargs)

class UserRegisterForm(forms.ModelForm):
    first_name = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'نام'}))
    last_name = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'نام خانوادگی'}))
    username = forms.CharField(widget=forms.TextInput(attrs={'placeholder': '  نام کاربری '}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': '  رمز عبور '}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={'placeholder':'ایمیل'}))
    class Meta:
        model = User
        fields = [
            'username',
            'email',
            'password',
            'first_name',
            'last_name'
        ]



class Edit_user_form(forms.ModelForm):
    first_name = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'نام','style':'width:400px'}))
    last_name = forms.CharField(widget=forms.TextInput(attrs={'placeholder': ' نام خانوادگی','style':'width:400px'}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={'placeholder':'ایمیل','style':'width:400px'}))
    class Meta:
        model = User
        fields =\
            [
                'first_name',
                'last_name',
                'email',
            ]


