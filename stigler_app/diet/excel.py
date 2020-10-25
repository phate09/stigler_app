import pandas as pd
import os
import sys

from .db_methods import *
from .models import *


def handle_df_macros(df):
    print(df)
    for item in df["name"]:
        create_type_if_not_exists(item)
    for index, row in df.iterrows():
        name_ = row["name"]
        price_ = row["price"]
        amount_ = row["amount"]
        calories = row["kcal"]
        carbs = row["carb"]
        prot = row["prot"]
        fat = row["fat"]
        create_product_if_not_exists("Aldi " + name_, price_, amount_, calories, carbs, prot, fat, name_)


def handle_df_recipes(df):
    print(df)
    for index, row in df.iterrows():
        name_ = row["name"]
        servings = row["servings"]
        create_recipe_if_not_exists(name_, servings)

def handle_df_ingredients(df):
    print(df)
    for index, row in df.iterrows():
        recipe_name = row["recipe name"]
        amount = row["amount"]
        type_name = row["type"]
        create_ingredient_if_not_exist(recipe_name,type_name,amount)