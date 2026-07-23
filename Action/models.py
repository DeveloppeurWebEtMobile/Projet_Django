from django.db import models
from django.utils import timezone

class StatutChoices(models.TextChoices):
    NON_REALISE = 'NON_REALISE', 'Non réalisé'
    EN_COURS = 'EN_COURS', 'En cours'
    REALISE = 'REALISE', 'Réalisé'

class PrioriteChoices(models.TextChoices):
    BASSE = 'BASSE', 'Basse'
    MOYENNE = 'MOYENNE', 'Moyenne'
    HAUTE = 'HAUTE', 'Haute'

class Action(models.Model):
    nom = models.CharField(max_length=255, verbose_name="Nom de l'action")
    description = models.TextField(blank=True, null=True, verbose_name="Description")
    statut = models.CharField(
        max_length=20, 
        choices=StatutChoices.choices, 
        default=StatutChoices.NON_REALISE,
        verbose_name="Statut"
    )
    date_creation = models.DateTimeField(default=timezone.now, verbose_name="Date de création")

    class Meta:
        ordering = ['-date_creation']
        verbose_name = "Action"
        verbose_name_plural = "Actions"

    def __str__(self):
        return f"{self.nom} - {self.get_statut_display()}"

    @property
    def total_activites(self):
        return self.activites.count()


class Activite(models.Model):
    action = models.ForeignKey(
        Action, 
        on_delete=models.CASCADE, 
        related_name='activites',
        verbose_name="Action parente"
    )
    nom = models.CharField(max_length=255, verbose_name="Nom de l'activité")
    description = models.TextField(blank=True, null=True, verbose_name="Description")
    statut = models.CharField(
        max_length=20, 
        choices=StatutChoices.choices, 
        default=StatutChoices.NON_REALISE,
        verbose_name="Statut"
    )
    date_creation = models.DateTimeField(default=timezone.now, verbose_name="Date de création")

    class Meta:
        ordering = ['-date_creation']
        verbose_name = "Activité"
        verbose_name_plural = "Activités"

    def __str__(self):
        return f"{self.nom} (Action: {self.action.nom})"

    @property
    def total_taches(self):
        return self.taches.count()


class Tache(models.Model):
    activite = models.ForeignKey(
        Activite, 
        on_delete=models.CASCADE, 
        related_name='taches',
        verbose_name="Activité parente"
    )
    nom = models.CharField(max_length=255, verbose_name="Nom de la tâche")
    description = models.TextField(blank=True, null=True, verbose_name="Description")
    statut = models.CharField(
        max_length=20, 
        choices=StatutChoices.choices, 
        default=StatutChoices.NON_REALISE,
        verbose_name="Statut"
    )
    priorite = models.CharField(
        max_length=20,
        choices=PrioriteChoices.choices,
        default=PrioriteChoices.MOYENNE,
        verbose_name="Priorité"
    )
    date_creation = models.DateTimeField(default=timezone.now, verbose_name="Date de création")

    class Meta:
        ordering = ['-date_creation']
        verbose_name = "Tâche"
        verbose_name_plural = "Tâches"

    def __str__(self):
        return f"{self.nom} (Activité: {self.activite.nom})"