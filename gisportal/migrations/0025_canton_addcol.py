# Generated by Django 5.1.1 on 2025-01-17 18:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gisportal', '0024_shpss_delete_shp_alter_parcelle_table'),
    ]

    operations = [
        migrations.AddField(
            model_name='canton',
            name='addcol',
            field=models.CharField(default='additional'),
            preserve_default=False,
        ),
    ]
