from django.db import models
from django.contrib.auth.models import User


class Patient(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=264, default="")
    email = models.EmailField(max_length=264, default="")

    def __str__(self):
        return self.name
