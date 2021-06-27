from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User


class Record(models.Model):
    # Record of a consultation with a doctor
    patient = models.ForeignKey(User, on_delete=models.CASCADE)
    # TYPE_CHOICES = (
    #     ('eye', 'Eye'),
    #     ('ear', 'Ear'),
    #     ('skin', 'Skin'),
    #     ('kidney', 'Kidney'),
    #     ('heart', 'Heart'),
    #     ('other', 'Other'),
    # )
    date = models.DateTimeField(default=timezone.now)
    doctor_name = models.CharField(max_length=100, blank=True)
    hospital_name = models.CharField(max_length=100, blank=True)
    ailment_type = models.CharField(max_length=100)


class RecordFile(models.Model):
    # Multiple files of a Record
    record = models.ForeignKey(Record, on_delete=models.CASCADE)
    file = models.FileField(upload_to='documents/%Y/%m/%d')