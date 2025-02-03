from django.db import models
from django.utils.timezone import now
from accounts.models import Account
from services.models import Service

class Review(models.Model):
    #by = models.ForeignKey(Account, on_delete=models.CASCADE)
    service = models.ForeignKey(Service, on_delete=models.CASCADE, related_name='Avaliacoes')
    title = models.CharField(max_length=100)
    desc = models.TextField()
    stars = models.PositiveSmallIntegerField()  # 0 a 5 estrelas
    date = models.DateField(default=now)

    def __str__(self):
        return f"{self.title} - {self.service.name}"
