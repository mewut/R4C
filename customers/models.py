from django.db import models
from robots.models import Robot

class Customer(models.Model):
    email = models.EmailField(max_length=255, unique=True)
    waiting_list = models.ManyToManyField(Robot, blank=True, related_name='waiting_list')

    def __str__(self):
        return self.email
    