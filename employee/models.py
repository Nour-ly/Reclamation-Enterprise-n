from django.db import models
from django.contrib.auth.models import User


class Category(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    icon = models.CharField(max_length=50, default='fa-file')

    def __str__(self):
        return self.name


class Complaint(models.Model):
    STATUS_CHOICES = [
        ('new', '🟡 Nouvelle'),
        ('in_progress', '🔵 En cours'),
        ('resolved', '🟢 Résolue'),
        ('rejected', '🔴 Rejetée'),
    ]

    employee = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
    title = models.CharField(max_length=200)
    description = models.TextField()
    attachment = models.FileField(upload_to='complaints/', blank=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='new')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


class Response(models.Model):
    complaint = models.ForeignKey(Complaint, on_delete=models.CASCADE, related_name='responses')
    agent = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Réponse à {self.complaint.title}"