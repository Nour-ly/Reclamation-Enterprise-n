from django.db import models


# 1. La table des Réclamations
class Reclamation(models.Model):
    STATUS_CHOICES = [
        ('En attente', 'En attente'),
        ('En cours', 'En cours de traitement'),
        ('Resolue', 'Résolue'),
        ('Rejetee', 'Rejetée'),
    ]
    PRIORITE_CHOICES = [
        ('Basse', 'Basse'),
        ('Moyenne', 'Moyenne'),
        ('Haute', 'Haute'),
    ]

    client_nom = models.CharField(max_length=150)
    titre = models.CharField(max_length=200)
    description = models.TextField()
    priorite = models.CharField(max_length=10, choices=PRIORITE_CHOICES, default='Moyenne')
    statut = models.CharField(max_length=20, choices=STATUS_CHOICES, default='En attente')
    agent_assigne = models.CharField(max_length=100, blank=True, null=True)  # Nom de l'agent connecté
    reponse_agent = models.TextField(blank=True, null=True)
    commentaire_interne = models.TextField(blank=True, null=True)
    date_creation = models.DateTimeField(auto_now_add=True)
    date_modification = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"#{self.id} - {self.titre} ({self.statut})"


# 2. La table Historique pour la traçabilité demandée
class HistoriqueAction(models.Model):
    reclamation = models.ForeignKey(Reclamation, on_delete=models.CASCADE, related_name='historiques')
    agent_nom = models.CharField(max_length=100)
    action_effectuee = models.CharField(max_length=255)  # Ex: "Changement de statut à En cours"
    date_action = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.agent_nom} - {self.action_effectuee} ({self.date_action})"