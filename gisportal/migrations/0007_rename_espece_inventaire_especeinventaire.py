# Generated by Django 5.1.3 on 2024-12-25 15:08

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('gisportal', '0006_espece_inventaire'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='espece_inventaire',
            new_name='EspeceInventaire',
        ),
    ]
