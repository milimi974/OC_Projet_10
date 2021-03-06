import json

from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.core.paginator import PageNotAnInteger, EmptyPage, Paginator
from django.http import HttpResponse

from django.shortcuts import render, redirect
from django.contrib.auth import (
    authenticate,
    get_user_model,
    login,
    logout,
    update_session_auth_hash)

# Create your views here.
from django.urls import reverse

import tools
from account.models import UserProduct
from product.models import Product
from .forms import UserRegisterForm, UserLoginForm, UserEditForm


# from product.mocks import  Product

# login view
def login_view(request):

    if request.user.is_authenticated:
        return redirect("/")
    next = request.GET.get('next')
    title = "Connexion"
    form = UserLoginForm(request.POST or None)
    if form.is_valid():
        username = form.cleaned_data.get("username")
        password = form.cleaned_data.get("password")
        user = authenticate(username=username, password=password)
        login(request, user)
        if next:
            return redirect(next)
        return redirect("/")

    context = {"form":form, "title": title}
    return render(request, 'account/form.html', context)


# logout view
def logout_view(request):
    # redirect homepage if already disconnected
    if not request.user.is_authenticated:
        return redirect("/")
    # Disconnect user
    logout(request)
    return render(request, 'account/logout.html')


# register view
def register_view(request):
    title = "inscription"
    form = UserRegisterForm(request.POST or None)
    # get reference to page to redirect after connection
    next = request.GET.get('next')

    # Create user if clean form data
    if form.is_valid():
        user = form.save(commit=False)
        pwd = form.cleaned_data.get('password')
        user.set_password(pwd)
        user.save()
        login(request, user)
        if next:
            return redirect(next)
        return redirect("/")

    context = {"form": form, "title": title}
    return render(request, 'account/form.html', context)


# login view
def edit_view(request):

    if not request.user.is_authenticated:
        return redirect("/")
    title = "Modification profil"
    form = UserEditForm(request.POST or None, instance=request.user)

    # Create user if clean form data
    if form.is_valid():
       user = form.save(commit=False)
       user.save()

    context = {"form":form, "title": title, "password": True}
    return render(request, 'account/form.html', context)


# login view
def change_password_view(request):

    if not request.user.is_authenticated:
        return redirect("/")
    title = "Modification password"

    if request.method == "POST":

        form = PasswordChangeForm(data=request.POST, user=request.user)
        # Create user if clean form data
        if form.is_valid():
            form.save()
            return redirect(reverse("edit_profile"))

    else:
        form = PasswordChangeForm(user=request.user)
        context = {"form":form, "title": title}
        return render(request, 'account/form.html', context)


# user profile view
def profile_view(request):
    title = "Profil"
    return render(request, 'account/profile.html', {"title": title})


@login_required(login_url='/user/login/')
def list_view(request):
    # user product substitutions
    title = "Mes aliments de substitution"
    #substitutions = Product.all()
    user_products = UserProduct.objects.all().order_by('id')

    # pagination
    paginator = Paginator(user_products, 12)
    page = request.GET.get('page')

    try:
        user_products = paginator.page(page)
    except PageNotAnInteger:
        user_products = paginator.page(1)
    except EmptyPage:
        user_products = paginator.page(paginator.num_pages)

    pagination = tools.pagination(user_products, 10)

    context = {
        'user_products': user_products,
        'title': title,
        'pagination': pagination
    }

    return render(request, 'account/user_list.html', context)


def save_view(request):
    data_json = {'status': 'error','message':'Produit déjà dans vos favoris.'}
    # if user are login
    if request.user.is_authenticated and request.is_ajax:
        # extract params from request
        product_id =  request.POST.get('id')
        substitution_id =  request.POST.get('sub_id')
        # if ids exists
        if product_id and substitution_id:
            # if substitution product already exist
            sub = Product.objects.get(pk=substitution_id)
            if sub:
                # if product assimilate to user
                user_product_qs, create = UserProduct.objects.get_or_create(product_id=product_id, user=request.user)
                # test if relation already exist none create
                qs = user_product_qs.substitutions.filter(pk=substitution_id)
                if not qs.exists():
                    # if no relation add entry
                    user_product_qs.substitutions.add(sub)
                    data_json = {'status': 'success', 'message': 'Produit ajouté dans vos favoris.'}

    # convert json answer
    data_json = json.dumps(data_json)
    mimetype = 'application/json'
    return HttpResponse(data_json, mimetype)

