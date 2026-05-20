from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

# Create your models here.
from django.db import models
from django.contrib.auth.models import User

# Catégorie des réclamations
class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


# Réclamation
class Complaint(models.Model):

    STATUS_CHOICES = [
        ('Nouvelle', 'Nouvelle'),
        ('En cours', 'En cours'),
        ('Résolue', 'Résolue'),
        ('Rejetée', 'Rejetée'),
    ]

    PRIORITY_CHOICES = [
        ('Faible', 'Faible'),
        ('Moyenne', 'Moyenne'),
        ('Urgente', 'Urgente'),
    ]

    title = models.CharField(max_length=200)
    description = models.TextField()

    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    employee = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='employee_complaints'
    )

    agent = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='agent_complaints'
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='Nouvelle'
    )

    priority = models.CharField(
        max_length=20,
        choices=PRIORITY_CHOICES,
        default='Moyenne'
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


# Profile utilisateur
class Profile(models.Model):
    ROLE_CHOICES = [
        ('admin', 'Admin'),
        ('agent', 'Agent'),
        ('employee', 'Employee'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)

    def __str__(self):
        return self.user.username

@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance, role='employee')


