from django.db import models

class Action(models.Model):
    # Utilisation de TextChoices pour une gestion propre des clés (DB) et des labels (Affichage)
    class Statut(models.TextChoices):
        NON_REALISE = 'NON_REALISE', 'Non réalisé'
        EN_COURS = 'EN_COURS', 'En cours'
        REALISE = 'REALISE', 'Réalisé'

    nom = models.CharField(max_length=255, verbose_name="Nom de l'action")
    statut = models.CharField(
        max_length=20, 
        choices=Statut.choices, 
        default=Statut.NON_REALISE,
        verbose_name="Statut"
    )

    class Meta:
        ordering = ['nom']  # Les actions sont triées par nom

    def __str__(self):
        return f"{self.nom} - {self.get_statut_display()}"