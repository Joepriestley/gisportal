# Generated by Django 5.1.1 on 2025-01-27 08:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('globeportal', '0011_region_superficie'),
    ]

    operations = [
        migrations.AddField(
            model_name='province',
            name='superficie',
            field=models.DecimalField(blank=True, decimal_places=3, max_digits=12, null=True),
        ),
    ]
