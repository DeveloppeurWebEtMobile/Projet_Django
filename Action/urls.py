from django.urls import path
from . import views

urlpatterns = [
    path("", views.liste_action, name="liste_action")
]