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
               path('products/', views.products, name="products"),
               path('user/', views.userPage, name="user_page"),
               path('customer/<str:pk>/', views.customer, name="customer"),
               path("create_order/", views.createOrder, name="create_order"),
               path("create_order2/<str:pk>/", views.createOrder2, name="create_order2"),
               path("update_order/<str:pk>/", views.updateOrder, name="update_order"),
               path("delete_order/<str:pk>/", views.deleteOrder, name="delete_order"),
               path("register/",views.registerPage,name="register"),
               path("login/",views.loginPage,name="login"),
               path("logout/",views.logoutUser,name="logout"),
               path("account/",views.accountSettings,name="account"),
               ]
