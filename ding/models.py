from django.db import models
from django.contrib.postgres.fields import ArrayField
# Create your models here.
class DingGroup(models.Model):
    name = models.CharField(max_length=100)
    access_token = models.CharField(max_length=100)
    secret = models.CharField(max_length=100)
    SNcode =  ArrayField(
                models.CharField(max_length=10, blank=True),
                size=50,
            )
    def __str__(self) -> str:
        return str(self.name)
