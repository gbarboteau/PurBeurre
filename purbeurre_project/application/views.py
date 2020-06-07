from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from django.utils.safestring import mark_safe
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate, logout
from .forms import SignUpForm, ConnexionForm
from .models import Aliment, Substitute
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator


# Create your views here.
def index(request):
    is_connected = True
    context = {'is_connected': is_connected}
    template = loader.get_template('application/index.html')
    return HttpResponse(template.render(context, request=request))

def account(request):
    error = False
    if request.method == "POST":
        form = ConnexionForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password"]
            user = authenticate(username=username, password=password)  
            if user:
                login(request, user) 
            else: 
                error = True
    else:
        form = ConnexionForm()
    template = loader.get_template('application/account.html')
    is_connected = request.user.is_authenticated
    context = {'form': form, 'is_connected': is_connected}
    return HttpResponse(template.render(context, request=request))

def create_account(request):
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
    template = loader.get_template('application/create-account.html')
    is_connected = request.user.is_authenticated
    context = {'form_sign_up': form_sign_up, 'is_connected': is_connected}
    return HttpResponse(template.render(context, request=request))

def logout_view(request):
    logout(request)
    return redirect('index')

@login_required
def search(request):
    query = request.GET.get('query')
    if not query:
        aliments = Aliment.objects.all()
    else:
        aliments = Aliment.objects.filter(name__icontains=query)
    if not aliments.exists():
        aliments = Aliment.objects.filter(category__icontains=query)
    title = "Résultats pour la requête %s"%query
    context = {
        'aliments': aliments,
        'title': title
    }
    template = loader.get_template('application/search.html')
    return HttpResponse(template.render(context, request=request))

@login_required
def add_product(request):
    query = request.POST.get('substitute_id', False)
    print(query)
    my_substitute = Aliment.objects.get(pk=query)
    this_substitute = Substitute(user_id=request.user, aliment_id=my_substitute)
    this_substitute.save()
    template = loader.get_template('application/index.html')
    context = {}
    # print(this_aliment.name)
    return HttpResponse(template.render(context,request=request))

@login_required
def aliment(request, aliment_id):
    this_aliment = Aliment.objects.get(pk=aliment_id)
    all_substitutes = Aliment.objects.filter(category=this_aliment.category).filter(nutriscore__lt=this_aliment.nutriscore)
    print(this_aliment.nutriscore)
    template = loader.get_template('application/aliment.html')
    context = {'this_aliment': this_aliment, 'all_substitutes': all_substitutes}
    return HttpResponse(template.render(context,request=request))

@login_required
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
