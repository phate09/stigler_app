from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class Objectives(models.Model):
    calories_max = models.FloatField()
    calories_min = models.FloatField()
    carbohydrates_max = models.FloatField()
    carbohydrates_min = models.FloatField()
    protein_max = models.FloatField()
    protein_min = models.FloatField()
    fat_max = models.FloatField()
    fat_min = models.FloatField()


GENDER = (('female', 'Female'), ('male', 'Male'), ('none', 'None'))


def default_new_objective():
    objective: Objectives = Objectives.objects.create(calories_max=2000, calories_min=1500, carbohydrates_max=170, carbohydrates_min=150, protein_max=170, protein_min=150, fat_max=40, fat_min=30)
    objective.save()
    return objective


class Customer(models.Model):
    user = models.OneToOneField(User, null=True, blank=True, on_delete=models.CASCADE)
    objectives = models.OneToOneField(Objectives, null=True, blank=True, on_delete=models.CASCADE, default=default_new_objective)
    name = models.CharField(max_length=200, null=True)
    phone = models.CharField(max_length=200, null=True, blank=True)
    email = models.CharField(max_length=200, null=True, blank=True)
    height = models.FloatField(blank=True, null=True)
    weight = models.FloatField(blank=True, null=True)
    gender = models.CharField(max_length=200, null=True, choices=GENDER)
    date_created = models.DateTimeField(auto_now_add=True, null=True)
    profile_pic = models.ImageField(default="logo2.png", null=True, blank=True)

    def __str__(self):
        return self.name


class Tag(models.Model):
    name = models.CharField(max_length=200, null=True)

    def __str__(self):
        return self.name


class Type(models.Model):
    name = models.CharField(max_length=200, null=True)

    def __str__(self):
        return self.name


UNIT = (('ml', 'ml'), ('g', 'g'), ('l', 'l'), ('kg', 'kg'), ('unit', 'unit'))


class Product(models.Model):
    name = models.CharField(max_length=200, null=True)
    price = models.FloatField()
    amount = models.FloatField()
    unit = models.CharField(max_length=200, null=True, choices=UNIT)
    calories = models.FloatField()
    carbohydrates = models.FloatField()
    protein = models.FloatField()
    fat = models.FloatField()
    type = models.ForeignKey(Type, null=True, blank=True, on_delete=models.SET_NULL)

    def __str__(self):
        return self.name
    @property
    def price_density(self):
        return self.price / self.amount


class Recipe(models.Model):
    name = models.CharField(max_length=200, null=True)
    servings = models.FloatField(default=1)
    tags = models.ManyToManyField(Tag, blank=True)

    def __str__(self):
        return self.name

    def tag_list(self):
        tags_msg = ""
        for t in self.tags:
            tags_msg += t.name + ", "
        tags_msg = tags_msg[:-2]
        return tags_msg

    def simpleMacros(self, num_servings=1, rounding=2, rounding_price=2) -> dict:
        recipe_summary = {"calories": 0, "carbohydrates": 0, "protein": 0, "fat": 0, "price": 0}
        for ingredient in self.ingredient_set.all():
            first_product: Product = ingredient.type.product_set.all()[0]
            amount_multiplier = ingredient.amount / 100  # per 100gr ingredient
            calories = first_product.calories * amount_multiplier
            carbohydrates = first_product.carbohydrates * amount_multiplier
            protein = first_product.protein * amount_multiplier
            fat = first_product.fat * amount_multiplier
            price = first_product.price_density * 100 * amount_multiplier
            recipe_summary["calories"] += calories
            recipe_summary["carbohydrates"] += carbohydrates
            recipe_summary["protein"] += protein
            recipe_summary["fat"] += fat
            recipe_summary["price"] += price
        recipe_summary["calories"] = round(recipe_summary["calories"] * num_servings / self.servings, rounding)
        recipe_summary["carbohydrates"] = round(recipe_summary["carbohydrates"] * num_servings / self.servings, rounding)
        recipe_summary["protein"] = round(recipe_summary["protein"] * num_servings / self.servings, rounding)
        recipe_summary["fat"] = round(recipe_summary["fat"] * num_servings / self.servings, rounding)
        recipe_summary["price"] = round(recipe_summary["price"] * num_servings / self.servings, rounding_price)
        return recipe_summary


class Ingredient(models.Model):
    recipe = models.ForeignKey(Recipe, null=True, on_delete=models.CASCADE)
    type = models.ForeignKey(Type, null=True, blank=True, on_delete=models.SET_NULL)
    amount = models.FloatField()
    unit = models.CharField(max_length=200, null=True, choices=UNIT)

    def __str__(self):
        return self.type.name
