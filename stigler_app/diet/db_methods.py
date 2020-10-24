from .models import *
from django.contrib.auth.models import Group


def create_tag_if_not_exists(name):
    if len(Tag.objects.filter(name=name)) == 0:
        Tag.objects.create(name=name).save()
        print(f"Created tag {name}")


def create_user_if_not_exists(username, group):
    if len(User.objects.filter(username=username)) == 0:
        user = User.objects.create_user(username=username, email=f"{username}@mail.com", password="stigler01")
        user.groups.add(Group.objects.get(name=group))
        user.save()
        customer = Customer.objects.create(name=username)
        customer.user = user
        customer.save()
        print(f"Created user {username} in group {group} ")


def create_group_if_not_exists(name):
    if len(Group.objects.filter(name=name)) == 0:
        print(f"Created {name} group")
        Group.objects.create(name=name).save()


def create_type_if_not_exists(name):
    query = Type.objects.filter(name=name)
    if len(query) == 0:
        print(f"Created {name} type")
        new_type = Type.objects.create(name=name)
        new_type.save()
        return new_type
    else:
        return query[0]


def create_product_if_not_exists(name, price, amount, calories, carbs, protein, fat, type_name, unit="g"):
    query = Product.objects.filter(name=name)
    if len(query) == 0:
        type = create_type_if_not_exists(type_name)
        product = Product()
        product.name = name
        product.price = price
        product.amount = amount
        product.calories = calories
        product.carbohydrates = carbs
        product.protein = protein
        product.fat = fat
        product.type = type
        product.unit = unit
        product.save()
        print(f"Created {name} product")
        return product
    else:
        return query[0]
