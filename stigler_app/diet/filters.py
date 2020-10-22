from django.forms import ModelForm
import django_filters
from django_filters import DateFilter, CharFilter
from .models import Ingredient


class IngredientFilter(django_filters.FilterSet):
    type__name = CharFilter(field_name="type__name", lookup_expr="icontains")

    # class Meta:
    #     model = Ingredient
    #     fields = "__all__"
