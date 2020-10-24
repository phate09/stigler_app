#!/usr/bin/env python

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
