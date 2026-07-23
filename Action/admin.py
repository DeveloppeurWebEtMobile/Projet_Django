from django.contrib import admin
from .models import Action, Activite, Tache

@admin.register(Action)
class ActionAdmin(admin.ModelAdmin):
    list_display = ('id', 'nom', 'statut', 'total_activites', 'date_creation')
    list_filter = ('statut', 'date_creation')
    search_fields = ('nom', 'description')

@admin.register(Activite)
class ActiviteAdmin(admin.ModelAdmin):
    list_display = ('id', 'nom', 'action', 'statut', 'total_taches', 'date_creation')
    list_filter = ('statut', 'date_creation', 'action')
    search_fields = ('nom', 'description', 'action__nom')

@admin.register(Tache)
class TacheAdmin(admin.ModelAdmin):
    list_display = ('id', 'nom', 'activite', 'priorite', 'statut', 'date_creation')
    list_filter = ('statut', 'priorite', 'date_creation', 'activite')
    search_fields = ('nom', 'description', 'activite__nom')
