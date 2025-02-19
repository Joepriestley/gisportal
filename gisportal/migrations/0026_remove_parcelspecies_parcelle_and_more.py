# Generated by Django 5.1.1 on 2025-01-17 18:12

import django.contrib.gis.db.models.fields
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gisportal', '0025_canton_addcol'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='parcelspecies',
            name='parcelle',
        ),
        migrations.RemoveField(
            model_name='pointcloudmetadata',
            name='id_parcelle',
        ),
        migrations.CreateModel(
            name='Parcellle',
            fields=[
                ('id_parcel', models.AutoField(primary_key=True, serialize=False)),
                ('Parcellle', models.CharField(max_length=255)),
                ('superficie', models.DecimalField(decimal_places=3, max_digits=12)),
                ('location', models.CharField(blank=True, max_length=255, null=True)),
                ('geometry', django.contrib.gis.db.models.fields.PolygonField(blank=True, null=True, srid=4326)),
                ('commune', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='gisportal.commune')),
                ('dfp', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='gisportal.dfp')),
                ('groupe', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='gisportal.groupe')),
            ],
        ),
        migrations.AddField(
            model_name='parcelspecies',
            name='Parcellle',
            field=models.ForeignKey(default='null', on_delete=django.db.models.deletion.PROTECT, to='gisportal.parcellle'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='pointcloudmetadata',
            name='id_Parcellle',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='gisportal.parcellle'),
        ),
        migrations.DeleteModel(
            name='Parcelle',
        ),
    ]
