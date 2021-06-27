from django.db import models
from django.contrib.auth.models import User
from Record.models import Record


class Medicine(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    start_date = models.DateField(blank=True)
    end_date = models.DateField(blank=True)
    TYPE_CHOICES = (
        ('day', 'Day'),
        ('week', 'Week'),
        ('month', 'Month'),
        ('hour', 'Hour'),
        ('year', 'Year'),
        ('other', 'Other'),
    )
    repeat_unit = models.CharField(max_length=100, choices=TYPE_CHOICES, default='day', blank=True)
    repeat_magnitude = models.IntegerField(blank=True)
    additional_info = models.CharField(max_length=1000, blank=True)
    record = models.ForeignKey(Record, on_delete=models.CASCADE, null=True)

    class Meta:
        ordering = ['start_date']


class Timing(models.Model):
    medicine = models.ForeignKey(Medicine, on_delete=models.CASCADE)
    timing = models.TimeField(blank=True)
