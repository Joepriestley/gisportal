# Generated by Django 5.1.3 on 2024-12-25 14:56

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gisportal', '0005_remove_species_geom'),
    ]

    operations = [
        migrations.CreateModel(
            name='espece_inventaire',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('circonference', models.FloatField()),
                ('num_total', models.IntegerField()),
                ('hauteur', models.FloatField()),
                ('id_parcelspecies', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='gisportal.parcelspecies')),
            ],
        ),
    ]