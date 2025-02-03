from django.db import models

# Create your models here.

class Category(models.Model):
    name = models.CharField('Nome', max_length=50)

    def __str__(self):
        return self.name

class Service(models.Model):
    SERVICES_CHOICES = [
        ('public', 'Público'),
        ('private', 'Privado'),
    ]

    img = models.ImageField(upload_to='services/logo/', blank=True, null=True)
    name = models.CharField('Nome', max_length=50)
    category = models.ForeignKey(Category, on_delete=models.DO_NOTHING)  # Exemplo: Saúde, Educação
    service = models.CharField(max_length=10, choices=SERVICES_CHOICES)

    def avgStarsReviews(self):
        reviews = self.reviews.all()
        return reviews.aggregate(models.Avg('stars'))['stars__avg'] or 0

    def countReviews(self):
        return self.reviews.count()

    def __str__(self):
        return self.name