from django import forms
from captcha.fields import CaptchaField
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login
from .models import Profile, Post


class UserRegisterForm(UserCreationForm):
	email = forms.EmailField()
	captcha = CaptchaField()
	class Meta:
		model = User
		fields = ['username', 'email', 'password1', 'password2']


class UserUpdateForm(forms.ModelForm):
	email = forms.EmailField()
	
	class Meta:
		model = User
		fields = ['username', 'email']


class UserLoginForm(forms.ModelForm):
	email = forms.EmailField()
	captcha = CaptchaField()
	class Meta:
		model = User
		fields = ['username', 'password']


class ProfileUpdateForm(forms.ModelForm):
	captcha = CaptchaField()
	class Meta:
		model = Profile
		fields = ['image']


class PostForm(forms.ModelForm):

	class Meta:
		model = Post
		fields = ['title', 'content']


#class CaptchaTestModelForm(forms.ModelForm):
 #   captcha = CaptchaField()
   # class Meta:
  #      model = MyModel

