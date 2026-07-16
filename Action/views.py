from django.shortcuts import render

# Create your views here.
def liste_action(request):
    return render(request, 'action/liste_action.html')