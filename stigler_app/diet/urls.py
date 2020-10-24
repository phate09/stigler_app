"""stigler_app URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path
from . import views

urlpatterns = [path('', views.home, name="home"),
               # path('products/', views.products, name="products"),
               path('recipes/', views.recipes, name="recipes"),
               path("user_settings/", views.userSettings, name="user_settings"),
               # path('user/', views.userPage, name="user_page"),
               path('view_recipe/<str:pk>/', views.view_recipe, name="view_recipe"),
               path("create_recipe/", views.createRecipe, name="create_recipe"),
               path("update_recipe/<str:pk>/", views.updateRecipe, name="update_recipe"),
               path("update_customer/<str:pk>/", views.updateCustomer, name="update_customer"),
               path("update_objectives/<str:pk>/", views.updateObjectives, name="update_objectives"),
               path("delete_recipe/<str:pk>/", views.deleteRecipe, name="delete_recipe"),
               path("create_type/", views.addType, name="create_type"),
               path("add_ingredient/<str:pk>/", views.addIngredient, name="add_ingredient"),
               path("update_ingredient/<str:pk>/", views.updateIngredient, name="update_ingredient"),
               path("delete_ingredient/<str:pk>/", views.deleteIngredient, name="delete_ingredient"),
               path("register/",views.registerPage,name="register"),
               path("login/",views.loginPage,name="login"),
               path("logout/",views.logoutUser,name="logout"),
               path("init/",views.init_data,name="init_db"),
               path("import_file/",views.upload_file,name = "import_file"),
               path("import_local/",views.handle_uploaded_file,name = "import_local")
               ]
