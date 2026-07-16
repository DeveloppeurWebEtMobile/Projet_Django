from django.urls import path
from Action import views

urlpatterns = [
    path("liste_action/", views.liste_action, name="liste_action"),
   
]