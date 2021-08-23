from django.db import models
from django.core.exceptions import ValidationError
# Create your models here.
from django_mysql.models import ListCharField
class DingGroup(models.Model):
    name = models.CharField(max_length=100, verbose_name='名称')
    access_token = models.CharField(max_length=100)
    secret = models.CharField(max_length=100)
    SNcode = models.TextField(max_length=500)  
    def __str__(self) -> str:
        return str(self.name)

    def save(self, *args, **kwargs):
        return super().save(*args, **kwargs)

class Location(models.Model):
    location = models.CharField(max_length=100, verbose_name='地址')
    SNcode = models.TextField(max_length=500)

    def get_sncode(self):
        return list([i.strip() for i in self.SNcode.split()])
