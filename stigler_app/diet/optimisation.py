from .models import *
import numpy as np
from scipy import optimize


def optimise_diet(customer: Customer, randomness=False):
    results = {"ids": [], "servings": [], "daily_cost": 0, "annual cost": 0}
    bounds: Objectives = customer.objectives
    ub = [bounds.calories_max, bounds.carbohydrates_max, bounds.protein_max, bounds.fat_max]
    lb = [bounds.calories_min, bounds.carbohydrates_min, bounds.protein_min, bounds.fat_min]
    ub = np.array(ub)
    lb = np.array(lb)
    print(f"ub:{ub}")
    print(f"lb:{lb}")
    recipes = Recipe.objects.all()
    macros_list = []
    price_list = []
    food_names = []
    ids_list = []
    for recipe in recipes:
        ids_list.append(recipe.id)
        food_names.append(recipe.name)
        macros: dict = recipe.simpleMacros()
        macros_array = np.array(list(macros.values()))
        price_value = macros_array[-1]
        macros_array = macros_array[:-1]
        macros_list.append(macros_array)
        price_list.append(price_value)
    macros_list = np.stack(macros_list)
    price_list = np.stack(price_list)
    ids_list = np.array(ids_list)
    # print(macros_list)
    if randomness:
        random_array = np.random.random(price_list.shape)
        print(f"random_array:{random_array}")
        c = random_array * np.array(price_list)
    else:
        c = np.array(price_list)
    A = np.transpose(macros_list)
    A2 = np.transpose(macros_list)
    A3 = np.concatenate((A, -A2))  # the negative sign allows the use of a lower bound
    b = np.concatenate((ub, -lb))  # the negative sign allows the use of a lower bound
    min_max_amounts = (0, None)
    # Minimisation problem with upper bound
    solution = optimize.linprog(c, A_ub=A3, b_ub=b, method='revised simplex', bounds=min_max_amounts)
    print(solution.x)
    print("\nShopping List:\n")
    daily_cost = 0
    total_macros = {"calories": 0, "carbohydrates": 0, "protein": 0, "fat": 0, "price": 0}
    for i in np.transpose(np.argwhere(solution.x > 1e-3))[0]:  # don't show negligible foods
        used_id = ids_list[i]
        results["ids"].append(used_id)
        results["servings"].append(solution.x[i])
        food_total_cost = round(solution.x[i] * price_list[i], 6)
        print(round(solution.x[i], 2), "servings ", food_names[i], "= £", food_total_cost)
        daily_cost += food_total_cost
        simple_macros = Recipe.objects.get(id=used_id).simpleMacros(solution.x[i])
        total_macros = sum_macros(total_macros, simple_macros)
        print(f"Macros: {simple_macros}")
    results["daily_cost"] = round(daily_cost, 2)
    results["annual_cost"] = round(daily_cost * 365.25, 2)
    results["total_macros"] = total_macros
    print("\nTotal daily cost = £", round(daily_cost, 2))
    print("\nTotal yearly cost = £", round(daily_cost * 365.25, 2))
    print("\nNutrient intake (g) with this diet:")
    print("------------------------------")
    nutrients_names = ["kCal", "Carbohydrates", "Protein", "Fat"]
    for j in range(len(nutrients_names)):
        nut = macros_list[:, j]
        xs = round(np.matmul(nut, solution.x), 1)
        print(nutrients_names[j], xs, "g" if j != 0 else "")
    print(results)
    return results


def recipes_total_macros(recipes, servings):
    macros_total = None
    for i in range(len(recipes)):
        macros: dict = recipes[i].simpleMacros(servings[i])
        if macros_total is None:
            macros_total = macros
        else:
            for val in macros.keys():
                macros_total[val] += macros[val]
    return macros_total


def sum_macros(macros1: dict, macros2: dict):
    macros_new = {}
    for key in macros1.keys():
        macros_new[key] = macros1[key] + macros2[key]
    return macros_new
