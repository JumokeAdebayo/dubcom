import logging
import os
from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group
from captcha.models import CaptchaStore
from captcha.helpers import captcha_image_url
from django.contrib.auth import views, authenticate, login, logout
from .forms import UserRegisterForm, UserUpdateForm, ProfileUpdateForm, UserLoginForm
from django_otp.decorators import otp_required
from .decorators import unauthenticated_user, allowed_users, admin_only

logger = logging.getLogger(__name__)

@unauthenticated_user
def register(request):
	if request.method == 'POST':
		form = UserRegisterForm(request.POST)
		if form.is_valid():
			user = form.save()
			username = form.cleaned_data.get('username')

			group = Group.objects.get(name='bloguser')
			user.groups.add(group)
			messages.success(request, f'Your account has been created, you can now login ' + username)
			#return redirect('account/login')
	else:
		form = UserRegisterForm()
	logger.debug(form)
	return render(request, 'users/register.html', {'form': form})


def login(request):
	if request.user.is_authenticated:
		return redirect ('ecommerce-home')
	else:
		if request.method == 'POST':
			username = request.POST.get('username')
			password = request.POST.get('password')

			user = authenticate(request, username=username, password=password)

			if user is not None:
				UserLoginForm(request, user)
				return redirect('ecommerce-home')
			else:
				messages.info(request, 'Username OR password is incorrect')

		context = {}
		return render(request, 'account/login.html', context)


@login_required
def profile(request):
	#if request.user.is_verified():
	if request.method == 'POST':
		u_form = UserUpdateForm(request.POST, instance=request.user)
		p_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
		if u_form.is_valid() and p_form.is_valid():
			u_form.save()
			p_form.save()
			messages.success(request, f'Your account has been updated')
			return redirect('profile')
	else:
		u_form = UserUpdateForm(instance=request.user)
		p_form = ProfileUpdateForm(instance=request.user.profile)
	context = {
		'u_form': u_form,
		'p_form': p_form
	}
	return render(request, 'users/profile.html', context)
	#else:
		#return redirect('ecommerce-home')

