from django.shortcuts import render

from Action.models import Action

# Create your views here.
def liste_action(request):
    return render(request, 'action/liste_action.html')

def ajouter_action(request):
    if request.method == "POST":
        nom_action = request.POST.get('nom')
        statut_action = request.POST.get('statut')
        nom = nom_action
        statut = statut_action # Supprimer les espaces avant et après le nom
        Action.objects.create(nom=nom_action, statut=statut_action)
        print("Ajoutez")
    return render(request, 'action/ajouter_action.html')
