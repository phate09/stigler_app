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
    if len(Type.objects.filter(name=name)) == 0:
        print(f"Created {name} type")
        Type.objects.create(name=name).save()