from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Comment, Post
from captcha.fields import CaptchaField


class CommentForm(forms.ModelForm):
	
	captcha = CaptchaField()
	class Meta:
		model = Comment
		fields = ('name', 'email', 'body')


class PostForm(forms.ModelForm):

	captcha = CaptchaField()
	class Meta:
		model = Post
		fields = ['title', 'content'] 