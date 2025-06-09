from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
from datetime import timedelta

class Accounts(AbstractUser):
    phone = models.CharField(max_length=20)
    is_service = models.BooleanField(default=False)
    is_block = models.BooleanField(default=False)

    REQUIRED_FIELDS = []
    USERNAME_FIELD = 'username'

    class Meta:
        verbose_name = 'Account'
        verbose_name_plural = 'Accounts'

class Categories(models.Model):
    desc = models.CharField(max_length=50)

    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.desc   

def photo_service_upload_to(instance, filename):
    return f'service/{instance.id}/{filename}'

class Service(models.Model):
    account = models.ForeignKey(Accounts, on_delete=models.CASCADE)
    photo = models.ImageField(upload_to=photo_service_upload_to, blank=True, null=True)
    name = models.CharField(max_length=100)
    category = models.ForeignKey(Categories, on_delete=models.CASCADE)
    about = models.TextField(blank=True, null=True)
    since = models.PositiveIntegerField()
    phone = models.CharField(max_length=20)
    site = models.CharField(max_length=50, blank=True, null=True)
    is_verified = models.BooleanField(default=False)

    class Meta:
        verbose_name = 'Service'
        verbose_name_plural = 'Services'

    def __str__(self):
        return self.name
    
class PasswordResetCode(models.Model):
    phone = models.CharField(max_length=20, unique=True)
    code = models.CharField(max_length=6)
    created_at = models.DateTimeField(auto_now_add=True)

    def is_expired(self):
        return timezone.now() > self.created_at + timedelta(minutes=10)