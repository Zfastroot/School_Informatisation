from django.db import models


class School(models.Model):
    name = models.CharField(max_length=255)
    city = models.CharField(max_length=100)
    address = models.TextField(blank=True)
    phone = models.CharField(max_length=30, blank=True)

    def __str__(self):
        return self.name
