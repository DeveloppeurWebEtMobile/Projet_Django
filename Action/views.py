from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Q
from django.contrib import messages
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from .models import Action, Activite, Tache
from .forms import ActionForm, ActiviteForm, TacheForm, InscriptionForm, ConnexionForm

# ==============================================================================
# VUES D'AUTHENTIFICATION
# ==============================================================================

def connexion_view(request):
    """
    Vue de connexion des utilisateurs.
    """
    if request.user.is_authenticated:
        return redirect('liste_action')

    if request.method == 'POST':
        form = ConnexionForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, f"Bienvenue, {user.first_name or user.username} !")
            next_url = request.GET.get('next')
            return redirect(next_url if next_url else 'liste_action')
        else:
            messages.error(request, "Nom d'utilisateur ou mot de passe incorrect.")
    else:
        form = ConnexionForm()

    return render(request, 'auth/connexion.html', {'form': form})


def inscription_view(request):
    """
    Vue d'inscription pour créer un compte utilisateur.
    """
    if request.user.is_authenticated:
        return redirect('liste_action')

    if request.method == 'POST':
        form = InscriptionForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, f"Votre compte a été créé avec succès. Bienvenue {user.username} !")
            return redirect('liste_action')
        else:
            messages.error(request, "Veuillez corriger les erreurs ci-dessous.")
    else:
        form = InscriptionForm()

    return render(request, 'auth/inscription.html', {'form': form})


def deconnexion_view(request):
    """
    Vue de déconnexion.
    """
    logout(request)
    messages.info(request, "Vous avez été déconnecté avec succès.")
    return redirect('connexion')


# ==============================================================================
# NIVEAU 1 : ACTIONS
# ==============================================================================

@login_required
def liste_action(request):
    """
    Affiche la liste de toutes les Actions avec support de recherche et formulaire de création.
    """
    query = request.GET.get('q', '').strip()
    actions = Action.objects.all()

    if query:
        actions = actions.filter(
            Q(nom__icontains=query) | Q(description__icontains=query)
        )

    form = ActionForm()

    if request.method == "POST":
        form = ActionForm(request.POST)
        if form.is_valid():
            action = form.save()
            messages.success(request, f"L'action '{action.nom}' a été créée avec succès.")
            return redirect('liste_action')

    context = {
        'actions': actions,
        'query': query,
        'form': form,
    }
    return render(request, 'action/liste_action.html', context)


@login_required
def ajouter_action(request):
    """
    Vue spécifique de création d'Action.
    """
    if request.method == "POST":
        form = ActionForm(request.POST)
        if form.is_valid():
            action = form.save()
            messages.success(request, f"L'action '{action.nom}' a été ajoutée.")
            return redirect('liste_action')
    else:
        form = ActionForm()

    return render(request, 'action/ajouter_action.html', {'form': form})


@login_required
def modifier_action(request, action_id):
    """
    Modifie une Action existante.
    """
    action = get_object_or_404(Action, id=action_id)
    if request.method == "POST":
        form = ActionForm(request.POST, instance=action)
        if form.is_valid():
            form.save()
            messages.success(request, f"L'action '{action.nom}' a été mise à jour.")
            return redirect('liste_action')
    else:
        form = ActionForm(instance=action)

    return render(request, 'action/modifier_action.html', {'form': form, 'action': action})


@login_required
def supprimer_action(request, action_id):
    """
    Supprime une Action.
    """
    action = get_object_or_404(Action, id=action_id)
    if request.method == "POST":
        nom = action.nom
        action.delete()
        messages.success(request, f"L'action '{nom}' et ses activités/tâches associées ont été supprimées.")
        return redirect('liste_action')

    return render(request, 'action/supprimer_action.html', {'action': action})


@login_required
def detail_action(request, action_id):
    """
    Consulte les détails d'une action ou redirige vers ses activités.
    """
    action = get_object_or_404(Action, id=action_id)
    return redirect('liste_activites', action_id=action.id)


# ==============================================================================
# NIVEAU 2 : ACTIVITÉS (liées à une Action)
# ==============================================================================

@login_required
def liste_activites(request, action_id):
    """
    Affiche la liste des Activités liées à une Action spécifique avec fil d'Ariane et recherche.
    """
    action_parente = get_object_or_404(Action, id=action_id)
    query = request.GET.get('q', '').strip()

    activites = action_parente.activites.all()

    if query:
        activites = activites.filter(
            Q(nom__icontains=query) | Q(description__icontains=query)
        )

    form = ActiviteForm()

    if request.method == "POST":
        form = ActiviteForm(request.POST)
        if form.is_valid():
            activite = form.save(commit=False)
            activite.action = action_parente
            activite.save()
            messages.success(request, f"L'activité '{activite.nom}' a été créée avec succès.")
            return redirect('liste_activites', action_id=action_parente.id)

    context = {
        'action': action_parente,
        'activites': activites,
        'query': query,
        'form': form,
    }
    return render(request, 'action/liste_activite.html', context)


@login_required
def modifier_activite(request, activite_id):
    """
    Modifie une Activité.
    """
    activite = get_object_or_404(Activite, id=activite_id)
    action_id = activite.action.id

    if request.method == "POST":
        form = ActiviteForm(request.POST, instance=activite)
        if form.is_valid():
            form.save()
            messages.success(request, f"L'activité '{activite.nom}' a été modifiée.")
            return redirect('liste_activites', action_id=action_id)
    else:
        form = ActiviteForm(instance=activite)

    return render(request, 'action/modifier_activite.html', {'form': form, 'activite': activite})


@login_required
def supprimer_activite(request, activite_id):
    """
    Supprime une Activité.
    """
    activite = get_object_or_404(Activite, id=activite_id)
    action_id = activite.action.id

    if request.method == "POST":
        nom = activite.nom
        activite.delete()
        messages.success(request, f"L'activité '{nom}' et ses tâches associées ont été supprimées.")
        return redirect('liste_activites', action_id=action_id)

    return render(request, 'action/supprimer_activite.html', {'activite': activite})


@login_required
def detail_activite(request, activite_id):
    """
    Redirige vers les tâches associées à cette activité.
    """
    activite = get_object_or_404(Activite, id=activite_id)
    return redirect('liste_taches', activite_id=activite.id)


# ==============================================================================
# NIVEAU 3 : TÂCHES (liées à une Activité)
# ==============================================================================

@login_required
def liste_taches(request, activite_id):
    """
    Affiche la liste des Tâches liées à une Activité spécifique avec fil d'Ariane à 3 niveaux et recherche.
    """
    activite_parente = get_object_or_404(Activite, id=activite_id)
    action_parente = activite_parente.action
    query = request.GET.get('q', '').strip()

    taches = activite_parente.taches.all()

    if query:
        taches = taches.filter(
            Q(nom__icontains=query) | Q(description__icontains=query)
        )

    form = TacheForm()

    if request.method == "POST":
        form = TacheForm(request.POST)
        if form.is_valid():
            tache = form.save(commit=False)
            tache.activite = activite_parente
            tache.save()
            messages.success(request, f"La tâche '{tache.nom}' a été créée avec succès.")
            return redirect('liste_taches', activite_id=activite_parente.id)

    context = {
        'action': action_parente,
        'activite': activite_parente,
        'taches': taches,
        'query': query,
        'form': form,
    }
    return render(request, 'action/liste_tache.html', context)


@login_required
def modifier_tache(request, tache_id):
    """
    Modifie une Tâche.
    """
    tache = get_object_or_404(Tache, id=tache_id)
    activite_id = tache.activite.id

    if request.method == "POST":
        form = TacheForm(request.POST, instance=tache)
        if form.is_valid():
            form.save()
            messages.success(request, f"La tâche '{tache.nom}' a été mise à jour.")
            return redirect('liste_taches', activite_id=activite_id)
    else:
        form = TacheForm(instance=tache)

    return render(request, 'action/modifier_tache.html', {'form': form, 'tache': tache})


@login_required
def supprimer_tache(request, tache_id):
    """
    Supprime une Tâche.
    """
    tache = get_object_or_404(Tache, id=tache_id)
    activite_id = tache.activite.id

    if request.method == "POST":
        nom = tache.nom
        tache.delete()
        messages.success(request, f"La tâche '{nom}' a été supprimée.")
        return redirect('liste_taches', activite_id=activite_id)

    return render(request, 'action/supprimer_tache.html', {'tache': tache})
