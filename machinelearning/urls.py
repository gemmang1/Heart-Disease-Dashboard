from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("notebook/", views.notebook, name="notebook"),
]