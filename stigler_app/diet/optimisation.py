from .models import *
import numpy as np
from scipy import optimize


def optimise_diet(customer: Customer):
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
    for recipe in recipes:
        food_names.append(recipe.name)
        macros: dict = recipe.simpleMacros()
        macros_array = np.array(list(macros.values()))
        price_value = macros_array[-1]
        macros_array = macros_array[:-1]
        macros_list.append(macros_array)
        price_list.append(price_value)
    macros_list = np.stack(macros_list)
    price_list = np.stack(price_list)
    # print(macros_list)
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
    for i in np.transpose(np.argwhere(solution.x > 1e-3))[0]:  # don't show negligible foods
        food_total_cost = round(solution.x[i] * price_list[i], 6)
        print(round(solution.x[i], 2), "servings ", food_names[i], "= £", food_total_cost)
        daily_cost += food_total_cost

    print("\nTotal daily cost = £", round(daily_cost, 2))
    print("\nTotal yearly cost = £", round(daily_cost * 365.25, 2))
    print("\nNutrient intake (g) with this diet:")
    print("------------------------------")
    nutrients_names = ["kCal", "Carbohydrates", "Protein", "Fat"]
    for j in range(len(nutrients_names)):
        nut = macros_list[:, j]
        xs = round(np.matmul(nut, solution.x), 1)
        print(nutrients_names[j], xs, "g" if j != 0 else "")
    return solution
