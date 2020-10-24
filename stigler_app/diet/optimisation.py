from .models import *
def optimise_diet(customer:Customer):
    bounds = customer.objectives
    recipes = Recipe.objects.all()
    for recipe in recipes:
        recipe.simpleMacros()