# Generated by Django 5.1.1 on 2025-01-24 16:33

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('globeportal', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='canton',
            old_name='number_groupe',
            new_name='num_groupe',
        ),
    ]
