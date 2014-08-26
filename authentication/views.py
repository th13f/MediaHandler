# coding=utf-8
from django.contrib import auth
from django.contrib.auth import authenticate, logout, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import render
from MusicHandler.settings import MEDIA_ROOT
from authentication.forms import *
from PIL import Image
from authentication.models import UserProfile


def login_view(request):
    error = None
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            user = authenticate(username=form.cleaned_data['username'], password=form.cleaned_data['password'])
            if user is None:
                error = 'login incorrect'
            else:
                login(request, user)

                #if request.REQUEST.get('next'):
                #    return HttpResponseRedirect(request.REQUEST.get('next'))

                return HttpResponseRedirect(reverse('media:index'))
    else:
        form = LoginForm()

    return render(request, 'authentication/login.html', {'form': form, 'error': error})


def register_view(request):
    error = None
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']

            if User.objects.filter(username=username).exists():
                error = 'Username already exist'
            else:
                User.objects.create_user(username=username,
                                         password=password)
                user = authenticate(username=username, password=password)
                login(request, user)
                profile = UserProfile(user=user, email='', preferences='')
                profile.save()
                #return HttpResponseRedirect(reverse('events:events_page', args=(1,)))          установка параметров
                return HttpResponseRedirect(reverse('media:index'))
    else:
        form = UserCreationForm()

    return render(request, 'authentication/register.html', {'form': form, 'error': error})


def logout_view(request):
    logout(request)

    return HttpResponseRedirect(reverse('authentication:login'))


@login_required
def profile_view(request):
    user = auth.get_user(request)
    profile = user.userprofile
    if request.method == 'GET':
        data = {
            'email': profile.email,
            'profile_id': profile.id,
            'preferences': profile.preferences
        }
        form = ProfileForm(data)
    else:
        form = ProfileForm(request.POST, request.FILES)

        if form.is_valid():
            profile.email = request.POST['email']
            profile.preferences = request.POST['preferences']
            if form.cleaned_data['profile_image'] is not None:
                profile.image = form.cleaned_data['profile_image']
                profile.image_thumb = form.cleaned_data['profile_image']

            profile.save()

            if profile.image_thumb.name != '':
                path = MEDIA_ROOT+profile.image_thumb.name
                im = Image.open(path)
                size = 100, 100
                im.thumbnail(size, Image.ANTIALIAS)
                im.save(path)

    return render(request, 'authentication/profile.html', {'form': form})