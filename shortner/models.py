from django.db import models

class urls(models.Model):
    url = models.URLField()
    uid = models.CharField(max_length=255,unique=True)
