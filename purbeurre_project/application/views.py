from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from django.utils.safestring import mark_safe
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate, logout
from .forms import SignUpForm
from django.shortcuts import render, redirect


# Create your views here.
def index(request):
    is_connected = True
    context = {'is_connected': is_connected}
    template = loader.get_template('application/index.html')
    return HttpResponse(template.render(context, request=request))

def account(request):
    # form_sign_in = SignInForm(request.POST)
    # print(form_sign_in.is_valid())
    # if form_sign_in.is_valid():
    #     username = form_sign_in.cleaned_data.get('username')
    #     password = form_sign_in.cleaned_data.get('password')
    #     print(username)
    #     print(password)
    #     user = authenticate(request, username=username, password=password)
    #     if user is not None:
    #         login(request, user)
    #     return redirect('index')
    # else:
    #     form_sign_in = SignInForm()
    form_sign_up = SignUpForm(request.POST)
    print(form_sign_up.is_valid())
    if form_sign_up.is_valid():
        form_sign_up.save()
        username = form_sign_up.cleaned_data.get('username')
        email = form_sign_up.cleaned_data.get('email')
        password = form_sign_up.cleaned_data.get('password1')
        user = authenticate(username=username, password=password)
        login(request, user)
        return redirect('index')
    else:
        form_sign_up = SignUpForm()
    template = loader.get_template('application/account.html')
    is_connected = request.user.is_authenticated
    context = {'form_sign_up': form_sign_up, 'is_connected': is_connected}
    return HttpResponse(template.render(context, request=request))

def logout_view(request):
    logout(request)
    return redirect('index')

def search(request):
    is_connected = request.user.is_authenticated
    context = {'is_connected': is_connected}
    template = loader.get_template('application/account.html')
    return HttpResponse(template.render(context, request=request))

def aliment(request, aliment_id):
    is_connected = request.user.is_authenticated
    context = {'is_connected': is_connected}
    template = loader.get_template('application/account.html')
    return HttpResponse(template.render(context, request=request))

def mesproduits(request):
    is_connected = True
    context = {'is_connected': is_connected}
    template = loader.get_template('application/account.html')
    return HttpResponse(template.render(context, request=request))

def about(request):
    is_connected = True
    context = {'is_connected': is_connected}
    template = loader.get_template('application/account.html')
    return HttpResponse(template.render(context, request=request))
