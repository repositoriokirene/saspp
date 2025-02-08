from django.db import models
from django.utils.timezone import now
from accounts.models import Account

class Review(models.Model):
    user = models.ForeignKey(
        Account,
        on_delete=models.CASCADE,
        related_name='reviews'
    )
    company = models.ForeignKey(
        Account,
        on_delete=models.CASCADE,
        related_name='company_reviews'
    )
    stars = models.PositiveSmallIntegerField(choices=[(i, i) for i in range(1, 6)])
    title = models.CharField(max_length=255)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} - {self.stars} estrelas"
    
class Response(models.Model):
    review = models.ForeignKey(
        Review,
        on_delete=models.CASCADE,
        related_name='response'
    )
    company = models.ForeignKey(
        Account,
        on_delete=models.CASCADE,
        related_name='responses'
    )
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Resposta para {self.review.title}"


