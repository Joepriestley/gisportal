# Generated by Django 5.1.1 on 2025-01-27 09:09

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('globeportal', '0012_province_superficie'),
    ]

    operations = [
        migrations.RenameField(
            model_name='province',
            old_name='id_province',
            new_name='id_provinc',
        ),
    ]
