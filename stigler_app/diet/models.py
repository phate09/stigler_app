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


def default_new_objective():
    objective: Objectives = Objectives.objects.create(calories_max=2000, calories_min=1500,
                                                      carbohydrates_max=170, carbohydrates_min=150,
                                                      protein_max = 170, protein_min = 150,
                                                      fat_max = 40,fat_min = 30)
    # objective.calories_max = 2000
    # objective.calories_min = 1500
    # objective.carbohydrates_max = 170
    # objective.carbohydrates_min = 150
    # objective.protein_max = 170
    # objective.protein_min = 150
    # objective.fat_max = 40
    # objective.fat_min = 30
    objective.save()
    return objective


class Customer(models.Model):
    user = models.OneToOneField(User, null=True, blank=True, on_delete=models.CASCADE)
    objectives = models.OneToOneField(Objectives, null=True, blank=True, on_delete=models.CASCADE, default=default_new_objective)
    name = models.CharField(max_length=200, null=True)
    phone = models.CharField(max_length=200, null=True, blank=True)
    email = models.CharField(max_length=200, null=True, blank=True)
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
    price = models.FloatField()
    amount = models.FloatField()
    unit = models.CharField(max_length=200, null=True, choices=UNIT)
    calories = models.FloatField()
    carbohydrates = models.FloatField()
    protein = models.FloatField()
    fat = models.FloatField()
    type = models.ForeignKey(Type, null=True, blank=True, on_delete=models.SET_NULL)

    @property
    def price_density(self):
        return self.price / self.amount


class Recipe(models.Model):
    name = models.CharField(max_length=200, null=True)
    tags = models.ManyToManyField(Tag, blank=True)

    def __str__(self):
        return self.name


class Ingredient(models.Model):
    recipe = models.ForeignKey(Recipe, null=True, on_delete=models.CASCADE)
    type = models.ForeignKey(Type, null=True, blank=True, on_delete=models.SET_NULL)
    amount = models.FloatField()
    unit = models.CharField(max_length=200, null=True, choices=UNIT)

    def __str__(self):
        return self.type.name
