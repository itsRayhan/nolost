from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("api/find-path/", views.find_path_api, name="find_path_api"),
]
