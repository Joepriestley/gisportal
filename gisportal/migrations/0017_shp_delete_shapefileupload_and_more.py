# Generated by Django 5.1.1 on 2025-01-15 17:36

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gisportal', '0016_delete_shp_canton_properties_commune_properties_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Shp',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('description', models.CharField(blank=True, max_length=1000)),
                ('file', models.FileField(upload_to='%Y/%m/%d')),
                ('date', models.DateField(blank=True, default=datetime.date.today)),
            ],
        ),
        migrations.DeleteModel(
            name='ShapefileUpload',
        ),
        migrations.RenameField(
            model_name='canton',
            old_name='geom',
            new_name='geometry',
        ),
        migrations.RenameField(
            model_name='commune',
            old_name='geom',
            new_name='geometry',
        ),
        migrations.RenameField(
            model_name='forest',
            old_name='geom',
            new_name='geometry',
        ),
        migrations.RenameField(
            model_name='groupe',
            old_name='geom',
            new_name='geometry',
        ),
        migrations.RenameField(
            model_name='parcelle',
            old_name='geom',
            new_name='geometry',
        ),
        migrations.RenameField(
            model_name='province',
            old_name='geom',
            new_name='geometry',
        ),
        migrations.RenameField(
            model_name='region',
            old_name='geom',
            new_name='geometry',
        ),
        migrations.RemoveField(
            model_name='commune',
            name='properties',
        ),
        migrations.RemoveField(
            model_name='forest',
            name='properties',
        ),
        migrations.RemoveField(
            model_name='groupe',
            name='properties',
        ),
        migrations.RemoveField(
            model_name='parcelle',
            name='properties',
        ),
        migrations.RemoveField(
            model_name='province',
            name='properties',
        ),
        migrations.AlterModelTable(
            name='parcelle',
            table='Parcelle',
        ),
    ]
