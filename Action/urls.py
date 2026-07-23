from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
from .forms import ReinitialiserMotDePasseForm, DefinirNouveauMotDePasseForm

urlpatterns = [
    # Authentification & Compte
    path('connexion/', views.connexion_view, name='connexion'),
    path('inscription/', views.inscription_view, name='inscription'),
    path('deconnexion/', views.deconnexion_view, name='deconnexion'),

    # Mot de passe oublié
    path('mot-de-passe-oublie/', auth_views.PasswordResetView.as_view(
        template_name='auth/mot_de_passe_oublie.html',
        form_class=ReinitialiserMotDePasseForm,
        email_template_name='auth/email_reinitialisation.html',
        subject_template_name='auth/email_sujet.txt'
    ), name='password_reset'),
    
    path('mot-de-passe-oublie/envoye/', auth_views.PasswordResetDoneView.as_view(
        template_name='auth/mot_de_passe_envoye.html'
    ), name='password_reset_done'),
    
    path('reinitialiser/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(
        template_name='auth/reinitialiser_mot_de_passe.html',
        form_class=DefinirNouveauMotDePasseForm
    ), name='password_reset_confirm'),
    
    path('reinitialiser/termine/', auth_views.PasswordResetCompleteView.as_view(
        template_name='auth/reinitialisation_terminee.html'
    ), name='password_reset_complete'),

    # Niveau 1 : Actions
    path('', views.liste_action, name='liste_action'),
    path('actions/ajouter/', views.ajouter_action, name='ajouter_action'),
    path('ajouter_action/', views.ajouter_action),
    path('actions/<int:action_id>/', views.detail_action, name='detail_action'),
    path('actions/<int:action_id>/modifier/', views.modifier_action, name='modifier_action'),
    path('actions/<int:action_id>/supprimer/', views.supprimer_action, name='supprimer_action'),

    # Niveau 2 : Activités
    path('actions/<int:action_id>/activites/', views.liste_activites, name='liste_activites'),
    path('activites/<int:activite_id>/', views.detail_activite, name='detail_activite'),
    path('activites/<int:activite_id>/modifier/', views.modifier_activite, name='modifier_activite'),
    path('activites/<int:activite_id>/supprimer/', views.supprimer_activite, name='supprimer_activite'),

    # Niveau 3 : Tâches
    path('activites/<int:activite_id>/taches/', views.liste_taches, name='liste_taches'),
    path('taches/<int:tache_id>/modifier/', views.modifier_tache, name='modifier_tache'),
    path('taches/<int:tache_id>/supprimer/', views.supprimer_tache, name='supprimer_tache'),
]