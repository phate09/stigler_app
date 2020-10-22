from django.contrib import admin

# Register your models here.
from .models import *

admin.site.register(Customer)
admin.site.register(Product)
admin.site.register(Tag)
admin.site.register(Objectives)
admin.site.register(Type)
admin.site.register(Recipe)
admin.site.register(Ingredient)