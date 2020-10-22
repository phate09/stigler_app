from django.forms import ModelForm
from .models import Ingredient, Customer, Recipe,Type
from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.contrib.auth.models import User
from django.contrib import admin


class CustomerForm(ModelForm):
    class Meta:
        model = Customer
        fields = '__all__'
        exclude = ['user']


class IngredientForm(ModelForm):
    class Meta:
        model = Ingredient
        fields = "__all__"
        widgets = {'recipe': forms.HiddenInput()}
class TypeForm(ModelForm):
    class Meta:
        model = Type
        fields = "__all__"


class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2"]


class CreateRecipeForm(forms.ModelForm):
    class Meta:
        model = Recipe
        fields = "__all__"


class CreateRecipeAdmin(admin.ModelAdmin):
    form = CreateRecipeForm
    filter_horizontal = ('tags',)