from django.db import models
from django.contrib.auth.models import AbstractUser

class Category(models.Model):
    desc = models.TextField(max_length=50)

class Account(AbstractUser):
    phone = models.CharField(max_length=10, blank=True, null=True)
    is_company = models.BooleanField(default=False)
    is_verify = models.BooleanField(default=False)
    company_name = models.CharField(max_length=100, blank=True, null=True)
    category = models.ForeignKey(Category, on_delete=models.DO_NOTHING, null=True, blank=True)
    address = models.CharField(max_length=100, blank=True, null=True)
    #photo = models.ImageField(upload_to= , blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = 'Accounts'
    
    def __str__(self):
        return f'{self.id} - {self.company_name}' if self.company_name else f'{self.id} - {self.first_name} {self.last_name}'