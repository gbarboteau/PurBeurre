from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from django.utils.safestring import mark_safe
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate, logout
from .forms import SignUpForm, ConnexionForm
from .models import Aliment, Substitute
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db import IntegrityError


def index(request):
    """Displays the index view"""
    is_connected = True
    context = {'is_connected': is_connected}
    template = loader.get_template('application/index.html')
    return HttpResponse(template.render(context, request=request))

def account(request):
    """Displays the account view and the user login form"""
    state = ""
    if request.method == "POST":
        form = ConnexionForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password"]
            user = authenticate(username=username, password=password)  
            if user:
                login(request, user) 
            else: 
                state = "Votre username ou mot de passe est incorrect."
        else: 
            print(form.errors)
    else:
        form = ConnexionForm()
    template = loader.get_template('application/account.html')
    is_connected = request.user.is_authenticated
    context = {'form': form, 'state': state}
    return HttpResponse(template.render(context, request=request))

def create_account(request):
    """Displays the create_account view and the user
    creation form
    """
    template = loader.get_template('application/create-account.html')
    context = {}
    if request.method == 'POST':
        form_sign_up = SignUpForm(request.POST)
        if form_sign_up.is_valid():
            form_sign_up.save()
            username = form_sign_up.cleaned_data.get('username')
            email = form_sign_up.cleaned_data.get('email')
            password = form_sign_up.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            login(request, user)
            return HttpResponse(template.render(context, request=request))
        else:
            print(form_sign_up.errors)
    else:
        form_sign_up = SignUpForm()
    is_connected = request.user.is_authenticated
    context = {'form_sign_up': form_sign_up, 'is_connected': is_connected}
    return HttpResponse(template.render(context, request=request))

def logout_view(request):
    """Log out the user and redirect the user to
    the index view
    """
    logout(request)
    return redirect('index')

@login_required
def search(request):
    """Displays the search view for a given query"""
    query = ""
    queryNum = 0
    if 'query1' in request.GET: #if the navbar form is filled
        query = request.GET.get('query1')
        queryNum = 1
    elif 'query2' in request.GET: #if the index page form is filled
        query = request.GET.get('query2')
        queryNum = 2
    if not query: #if no form is filled
        aliments = Aliment.objects.all()
    else:
        aliments = Aliment.objects.filter(name__icontains=query)
    if not aliments.exists():
        aliments = Aliment.objects.filter(category__icontains=query)
    paginator = Paginator(aliments, 9)
    page = request.GET.get('page')
    try:
        aliments = paginator.page(page)
    except PageNotAnInteger:
        aliments = paginator.page(1)
    except EmptyPage:
        aliments = paginator.page(paginator.num_pages)
    title = "Résultats pour la requête %s"%query
    context = {'aliments': aliments, 'title': title, 'paginate': True, 'query': query, 'queryNum': queryNum}
    template = loader.get_template('application/search.html')
    return HttpResponse(template.render(context, request=request))

@login_required
def add_product(request, aliment_id):
    """Displays the add_product view and adds
    a substitute to a user's list
    """
    my_substitute = get_object_or_404(Aliment, pk=aliment_id)
    try:
        this_substitute = Substitute(user_id=request.user, aliment_id=my_substitute)
        this_substitute.save()
        context = {'is_added': True}
    except IntegrityError as error:
        context = {'is_added': False}
    template = loader.get_template('application/add-product.html')
    return HttpResponse(template.render(context,request=request))

@login_required
def remove_product(request, aliment_id):
    """Displays the remove_product view and removes
    a substitute from a user's list
    """
    my_substitute = get_object_or_404(Substitute, user_id=request.user, aliment_id=aliment_id)
    try:
        my_substitute.delete()
        context = {'is_deleted': True}
    except IntegrityError as error:
        context = {'is_deleted': False}
    template = loader.get_template('application/remove-product.html')
    return HttpResponse(template.render(context,request=request))

@login_required
def aliment(request, aliment_id):
    """Displays the aliment view for a
    given product
    """
    this_aliment = get_object_or_404(Aliment, pk=aliment_id)
    all_substitutes = Aliment.objects.filter(category=this_aliment.category).filter(nutriscore__lt=this_aliment.nutriscore)
    print(this_aliment.nutriscore)
    template = loader.get_template('application/aliment.html')
    context = {'this_aliment': this_aliment, 'all_substitutes': all_substitutes}
    return HttpResponse(template.render(context,request=request))

@login_required
def mesproduits(request):
    """Displays the mesproduits view and all the substitutes
    for the connected user
    """
    user_id = request.user.id
    my_substitutes = Substitute.objects.filter(user_id=user_id)
    id_substitute_list = Substitute.objects.filter(user_id=user_id).values_list('aliment_id', flat=True)
    aliments = Aliment.objects.filter(pk__in=id_substitute_list)
    is_connected = True
    context = {'aliments': aliments, 'is_connected': is_connected}
    template = loader.get_template('application/mesproduits.html')
    return HttpResponse(template.render(context, request=request))

def mentionslegales(request):
    """Displays the mentionslegales view"""
    context = {}
    template = loader.get_template('application/mentionslegales.html')
    return HttpResponse(template.render(context, request=request))