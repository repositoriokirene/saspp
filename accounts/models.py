from django.db import models
from django.contrib.auth.models import AbstractUser

class Account(AbstractUser):
    PROFILES_CHOICES = [
        ('retail', 'Particular'),
        ('corporate', 'Empresa'),
    ]
    profile = models.CharField('Perfil' , max_length=50, choices=PROFILES_CHOICES, default='retail')