# Generated by Django 5.1.3 on 2024-12-25 16:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gisportal', '0008_rename_num_total_especeinventaire_num_total_arbre_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='especeinventaire',
            name='volume_total_arbre',
            field=models.DecimalField(blank=True, decimal_places=3, max_digits=7, null=True),
        ),
    ]
