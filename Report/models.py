from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from Record.models import Record


class Report(models.Model):
    # Test Reports
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateTimeField(default=timezone.now)
    test_name = models.CharField(max_length=100)
    record = models.ForeignKey(Record, on_delete=models.CASCADE)


class ReportFile(models.Model):
    # Multiple files of a Record
    report = models.ForeignKey(Report, on_delete=models.CASCADE)
    file = models.FileField(upload_to='documents/%Y/%m/%d')
