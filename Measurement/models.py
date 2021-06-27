from django.db import models
# from django.utils import timezone
from django.contrib.auth.models import User


class MeasurementGroup(models.Model):
    # A Test Measure Grouping, such as Blood Sugar, Cholesterol, etc.
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    unit = models.CharField(max_length=100)
    lower_bound = models.DecimalField(max_digits=10, decimal_places=4)
    upper_bound = models.DecimalField(max_digits=10, decimal_places=4)


class Measurement(models.Model):
    # A measurement for the given measurement group. For e.g., Group: Blood Sugar, Value: 100mg/dL for 1st Aug, 2020
    date = models.DateTimeField()
    magnitude = models.DecimalField(max_digits=10, decimal_places=4)
    group = models.ForeignKey(MeasurementGroup, on_delete=models.CASCADE)
