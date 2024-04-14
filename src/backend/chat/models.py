from django.db import models


class Settings(models.Model):
    model = models.CharField(max_length=100)
    provider = models.CharField(max_length=100)
    key = models.CharField(max_length=100)

    def __str__(self):
        return self.model
