from django.db import models

STATUT_CHOICES = {
    'Nonrealise' : 'Non réalisé',
    'Encours' : 'En cours',
    'Realise' : 'Réalisé',
}

# Create your models here.
class Action(models.Model):
    nom = models.CharField(max_length=255,blank=True)
    statut = models.CharField(max_length=255, choices=STATUT_CHOICES, default='Non réalisé')

    def _str_(self):
        return f"{self.nom} - {self.statut}"