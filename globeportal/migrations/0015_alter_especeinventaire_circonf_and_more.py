# Generated by Django 5.1.1 on 2025-01-27 10:02

import datetime
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('globeportal', '0014_alter_canton_canton_nam_alter_canton_geometry_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='especeinventaire',
            name='circonf',
            field=models.FloatField(blank=True, db_column='circonf', null=True),
        ),
        migrations.AlterField(
            model_name='especeinventaire',
            name='hauteur',
            field=models.FloatField(blank=True, db_column='hauteur', null=True),
        ),
        migrations.AlterField(
            model_name='especeinventaire',
            name='id_parcspp',
            field=models.ForeignKey(blank=True, db_column='id_parcspp', null=True, on_delete=django.db.models.deletion.CASCADE, to='globeportal.parcelspecies'),
        ),
        migrations.AlterField(
            model_name='especeinventaire',
            name='num_arbre',
            field=models.IntegerField(blank=True, db_column='num_arbre', null=True),
        ),
        migrations.AlterField(
            model_name='especeinventaire',
            name='vol_arbre',
            field=models.FloatField(blank=True, db_column='vol_arbre', null=True),
        ),
        migrations.AlterField(
            model_name='parcelspecies',
            name='num_species',
            field=models.IntegerField(blank=True, db_column='num_species', null=True),
        ),
        migrations.AlterField(
            model_name='parcelspecies',
            name='num_total',
            field=models.IntegerField(blank=True, db_column='num_total', null=True),
        ),
        migrations.AlterField(
            model_name='parcelspecies',
            name='parcelle',
            field=models.ForeignKey(db_column='parcelle', on_delete=django.db.models.deletion.PROTECT, to='globeportal.parcelle'),
        ),
        migrations.AlterField(
            model_name='parcelspecies',
            name='sci_name',
            field=models.ForeignKey(db_column='sci_name', on_delete=django.db.models.deletion.PROTECT, to='globeportal.species'),
        ),
        migrations.AlterField(
            model_name='parcelspecies',
            name='vol_total',
            field=models.FloatField(blank=True, db_column='vol_total', null=True),
        ),
        migrations.AlterField(
            model_name='pointcloudmetadata',
            name='date',
            field=models.DateField(blank=True, db_column='date', default=datetime.date.today, null=True),
        ),
        migrations.AlterField(
            model_name='pointcloudmetadata',
            name='id_parcel',
            field=models.ForeignKey(blank=True, db_column='id_parcel', null=True, on_delete=django.db.models.deletion.CASCADE, to='globeportal.parcelle'),
        ),
        migrations.AlterField(
            model_name='pointcloudmetadata',
            name='responsable',
            field=models.CharField(blank=True, db_column='responsable', max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='pointcloudmetadata',
            name='threeD_mod',
            field=models.URLField(blank=True, db_column='threeD_mod', null=True),
        ),
        migrations.AlterField(
            model_name='species',
            name='french_name',
            field=models.CharField(blank=True, db_column='french_name', max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='species',
            name='id_species',
            field=models.AutoField(db_column='id_species', primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='species',
            name='sci_name',
            field=models.CharField(blank=True, db_column='sci_name', max_length=255),
        ),
        migrations.AlterField(
            model_name='species',
            name='spp_descript',
            field=models.TextField(blank=True, db_column='spp_descript', null=True),
        ),
        migrations.AlterField(
            model_name='species',
            name='vernac_name',
            field=models.CharField(blank=True, db_column='vernac_name', max_length=255, null=True),
        ),
    ]
