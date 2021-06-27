from django.db import models
from django.contrib.auth.models import User


class Allergy(models.Model):
    # To describe one's allergies like sneezing due to dust.
    description = models.CharField(max_length=200)
    cause = models.CharField(max_length=200)
    symptoms = models.TextField(max_length=200)
    additional_notes = models.TextField(max_length=200)
    medicine = models.CharField(max_length=100) # models.ForeignKey()
    user = models.ForeignKey(User,on_delete=models.CASCADE)

