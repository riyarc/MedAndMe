from django.contrib import admin
from .models import MeasurementGroup, Measurement

admin.site.register(MeasurementGroup)
admin.site.register(Measurement)
