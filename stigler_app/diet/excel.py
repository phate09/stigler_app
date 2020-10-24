import pandas as pd
import os
# from django.conf import settings
# DATABASES = {'default': {'ENGINE': 'django.db.backends.sqlite3', 'NAME': "/home/edoardo/Development/stigler_app/stigler_app/db.sqlite3", }}
# settings.configure(DATABASES)
# from stigler_app.diet.models import Recipe


def handle_df(df):
    print(df)
    del df["Recipe link"]
    column_names = df.columns.values.tolist()
    last_recipe = None
    for row in df.rows:
        tag = row["Tag"]
        name = row["Recipe Name"]
        servings = row["Servings"]
        ingredient = row["Ingredients"]
        amount = row["Amount"]
        unit = row["Unit"]
        if pd.notnull(name):
            last_recipe = Recipe()
            last_recipe.name = name
            last_recipe.servings = servings
        # if pd.notnull(ingredient):


if __name__ == '__main__':
    pd.options.display.max_columns = 10
    from django.conf import settings

    df = pd.read_excel("/home/edoardo/Development/stigler_app/stigler_app/import.xlsx")
    handle_df(df)
