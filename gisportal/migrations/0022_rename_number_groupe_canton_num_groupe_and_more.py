# Generated by Django 5.1.1 on 2025-01-17 09:14

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('gisportal', '0021_remove_shp_keyy_shp_model_type'),
    ]

    operations = [
        migrations.RenameField(
            model_name='canton',
            old_name='number_groupe',
            new_name='num_groupe',
        ),
        migrations.RenameField(
            model_name='canton',
            old_name='surface_area',
            new_name='superficie',
        ),
        migrations.RenameField(
            model_name='especeinventaire',
            old_name='circonference',
            new_name='circonf',
        ),
        migrations.RenameField(
            model_name='especeinventaire',
            old_name='id_parcelspecies',
            new_name='id_parcespp',
        ),
        migrations.RenameField(
            model_name='especeinventaire',
            old_name='num_total_arbre',
            new_name='num_arbre',
        ),
        migrations.RenameField(
            model_name='especeinventaire',
            old_name='volume_total_arbre',
            new_name='vol_arbre',
        ),
        migrations.RenameField(
            model_name='forest',
            old_name='forest_formation',
            new_name='for_formatio',
        ),
        migrations.RenameField(
            model_name='forest',
            old_name='location_name',
            new_name='loca_name',
        ),
        migrations.RenameField(
            model_name='forest',
            old_name='number_canton',
            new_name='num_canton',
        ),
        migrations.RenameField(
            model_name='forest',
            old_name='number_parcel',
            new_name='num_parcel',
        ),
        migrations.RenameField(
            model_name='forest',
            old_name='surface_area',
            new_name='superficie',
        ),
        migrations.RenameField(
            model_name='forest',
            old_name='titre_foncier',
            new_name='titre_fonci',
        ),
        migrations.RenameField(
            model_name='groupe',
            old_name='parcel_number',
            new_name='parcel_num',
        ),
        migrations.RenameField(
            model_name='groupe',
            old_name='surface_area',
            new_name='superficie',
        ),
        migrations.RenameField(
            model_name='parcelspecies',
            old_name='scientific_name',
            new_name='sci_name',
        ),
        migrations.RenameField(
            model_name='parcelspecies',
            old_name='volume_total',
            new_name='vol_total',
        ),
        migrations.RenameField(
            model_name='pointcloudmetadata',
            old_name='date_collection',
            new_name='date_collec',
        ),
        migrations.RenameField(
            model_name='pointcloudmetadata',
            old_name='collecteur',
            new_name='responsable',
        ),
        migrations.RenameField(
            model_name='pointcloudmetadata',
            old_name='threeD_modellink',
            new_name='threeD_mod',
        ),
        migrations.RenameField(
            model_name='species',
            old_name='scientific_name',
            new_name='sci_name',
        ),
        migrations.RenameField(
            model_name='species',
            old_name='species_importance',
            new_name='spp_decript',
        ),
        migrations.RenameField(
            model_name='species',
            old_name='vernacular_name',
            new_name='vernac_name',
        ),
    ]
