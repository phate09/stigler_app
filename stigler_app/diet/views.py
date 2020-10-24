from django.http import HttpResponse, HttpResponseRedirect

from .db_methods import create_tag_if_not_exists, create_group_if_not_exists, create_user_if_not_exists, create_type_if_not_exists
from .forms import CreateUserForm, UploadFileForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import Group
from django.shortcuts import render, redirect
from django.contrib import messages
from .decorators import unauthenticated_user, allowed_users
from .models import *
from .forms import CreateRecipeForm, IngredientForm, TypeForm, UpdateCustomerForm, UpdateObjectivesForm
from .filters import IngredientFilter
from django.contrib.auth.decorators import login_required


# Create your views here.
@unauthenticated_user
def registerPage(request):
    form = CreateUserForm()
    if request.method == "POST":
        form = CreateUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get("username")
            group = Group.objects.get(name='customer')
            user.groups.add(group)
            Customer.objects.create(user=user, name=username)
            messages.success(request, f"Account was created for {username}")
            return redirect("login")

    context = {"form": form}
    return render(request, 'diet/register.html', context)


@unauthenticated_user
def loginPage(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.info(request, "Username or password is incorrect")
    context = {}
    return render(request, 'diet/login.html', context)


def logoutUser(request):
    logout(request)
    return redirect("login")


@login_required(login_url="login")
# @allowed_users(allowed_roles=["admin"])
def home(request):
    context = {}
    return render(request, "diet/dashboard.html", context)


@login_required(login_url="login")
# @allowed_users(allowed_roles=["admin"])
def userSettings(request):
    form = CreateUserForm()
    customer = Customer.objects.get(user=request.user)
    objectives = customer.objectives
    context = {'form': form, 'objectives': objectives, 'customer': customer}
    return render(request, "diet/user_settings.html", context)


@login_required(login_url="login")
@allowed_users(allowed_roles=["admin"])
def createRecipe(request):
    form = CreateRecipeForm()
    if request.method == "POST":
        form = CreateRecipeForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('recipes')
    context = {'form': form}
    return render(request, 'diet/recipe_form.html', context)


@login_required(login_url="login")
@allowed_users(allowed_roles=["admin"])
def updateRecipe(request, pk):
    recipe = Recipe.objects.get(id=pk)
    form = CreateRecipeForm(instance=recipe)
    if request.method == "POST":
        # print(request.POST)
        form = CreateRecipeForm(request.POST, instance=recipe)
        if form.is_valid():
            form.save()
            return redirect('recipes')
    context = {'form': form}
    return render(request, 'diet/recipe_form.html', context)


@login_required(login_url="login")
# @allowed_users(allowed_roles=["admin"])
def updateCustomer(request, pk):
    recipe = Customer.objects.get(id=pk)
    form = UpdateCustomerForm(instance=recipe)
    if request.method == "POST":
        form = UpdateCustomerForm(request.POST, instance=recipe)
        if form.is_valid():
            form.save()
            return redirect('user_settings')
    context = {'form': form}
    return render(request, 'diet/customer_form.html', context)


@login_required(login_url="login")
# @allowed_users(allowed_roles=["admin"])
def updateObjectives(request, pk):
    recipe = Objectives.objects.get(id=pk)
    form = UpdateObjectivesForm(instance=recipe)
    if request.method == "POST":
        form = UpdateObjectivesForm(request.POST, instance=recipe)
        if form.is_valid():
            form.save()
            return redirect('user_settings')
    context = {'form': form}
    return render(request, 'diet/objectives_form.html', context)


@login_required(login_url="login")
@allowed_users(allowed_roles=["admin"])
def deleteRecipe(request, pk):
    recipe = Recipe.objects.get(id=pk)
    if request.method == "POST":
        recipe.delete()
        return redirect('recipes')
    context = {'item': recipe}
    return render(request, 'diet/delete_recipe.html', context)


@login_required(login_url="login")
# @allowed_users(allowed_roles=["admin"])
def view_recipe(request, pk):
    recipe = Recipe.objects.get(id=pk)
    ingredients = recipe.ingredient_set.all()
    tags = recipe.tags.all()
    ingredients_count = recipe.ingredient_set.all().count()
    myFilter = IngredientFilter(request.GET, queryset=ingredients)
    ingredients = myFilter.qs
    context = {'recipe': recipe, 'ingredients': ingredients, 'ingredients_count': ingredients_count, 'myFilter': myFilter, "tags": tags}
    return render(request, "diet/recipe.html", context)


@login_required(login_url="login")
@allowed_users(allowed_roles=["admin"])
def addIngredient(request, pk):
    recipe = Recipe.objects.get(id=pk)
    form = IngredientForm(initial={'recipe': recipe})
    if request.method == "POST":
        # print(request.POST)
        form = IngredientForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/')
    context = {'form': form}
    return render(request, 'diet/ingredient_form.html', context)


@login_required(login_url="login")
@allowed_users(allowed_roles=["admin"])
def addType(request):
    form = TypeForm()
    if request.method == "POST":
        form = TypeForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/')
    context = {'form': form}
    return render(request, 'diet/type_form.html', context)


@login_required(login_url="login")
@allowed_users(allowed_roles=["admin"])
def updateIngredient(request, pk):
    order = Ingredient.objects.get(id=pk)
    form = IngredientForm(instance=order)
    if request.method == "POST":
        form = IngredientForm(request.POST, instance=order)
        if form.is_valid():
            form.save()
            return redirect('/')
    context = {'form': form}
    return render(request, 'diet/ingredient_form.html', context)


@login_required(login_url="login")
@allowed_users(allowed_roles=["admin"])
def deleteIngredient(request, pk):
    order = Ingredient.objects.get(id=pk)
    if request.method == "POST":
        order.delete()
        return redirect('/')
    context = {'item': order}
    return render(request, 'diet/delete_ingredient.html', context)


@login_required(login_url="login")
# @allowed_users(allowed_roles=["admin"])
def recipes(request):
    recipes = Recipe.objects.all()
    return render(request, "diet/recipes.html", {'recipes': recipes})

@login_required(login_url="login")
# @allowed_users(allowed_roles=["admin"])
def products(request):
    products = Product.objects.all()
    return render(request, "diet/products.html", {'products': products})

@login_required(login_url="login")
# @allowed_users(allowed_roles=["admin"])
def types(request):
    types = Type.objects.all()
    return render(request, "diet/types.html", {'types': types})


def init_data(request):
    create_group_if_not_exists("admin")
    create_group_if_not_exists("customer")
    create_user_if_not_exists("alessandra", "admin")
    create_user_if_not_exists("olivia", "admin")
    create_user_if_not_exists("edoardo", "admin")
    create_tag_if_not_exists("Vegetarian")
    create_tag_if_not_exists("Vegan")
    create_tag_if_not_exists("Gluten-Free")
    types = ["Flour", "Sugar", "Eggs", "Chicken", "Beef", "Carrots", "Onions", "Celery", "Pasta", "Oil", "Butter", "Tuna", "Apricot", "Pineapple", "Peas", "Beans"]
    for t in types:
        create_type_if_not_exists(t)
    return HttpResponse("Database has been filled with default values")


def upload_file(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            handle_uploaded_file(request.FILES['file'])
            return HttpResponseRedirect('/')
    else:
        form = UploadFileForm()
    return render(request, 'upload_file.html', {'form': form})


def handle_uploaded_file(f):
    print(type(f))
    # with open('some/file/name.txt', 'wb+') as destination:
    #     for chunk in f.chunks():
    #         destination.write(chunk)
