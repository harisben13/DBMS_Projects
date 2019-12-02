from django.urls import path
from . import views

urlpatterns=[
    path("register",views.register,name="register"),
    path("login",views.login,name="login"),
    path("logout",views.logout,name="logout"),
    path("search",views.search,name="search"),
    path("additems",views.additems,name="additems"),
    path("update",views.update,name="update")
]
