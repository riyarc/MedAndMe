# Generated by Django 3.2 on 2021-04-16 12:43

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='MeasurementGroup',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('unit', models.CharField(max_length=100)),
                ('lower_bound', models.DecimalField(decimal_places=4, max_digits=10)),
                ('upper_bound', models.DecimalField(decimal_places=4, max_digits=10)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Measurement',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateTimeField()),
                ('magnitude', models.DecimalField(decimal_places=4, max_digits=10)),
                ('group', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Measurement.measurementgroup')),
            ],
        ),
    ]
