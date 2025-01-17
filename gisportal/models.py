from django.db import models  # type: ignore
from django.contrib.gis.gdal import DataSource  # type: ignore
from django.contrib.gis.geos import GEOSGeometry  # type: ignore
from django.db.models import JSONField 
from django.contrib.gis.db import models as gis_model  # type: ignore
from django.core.exceptions import ValidationError  # type: ignore
import datetime 

from decouple import config
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
import geopandas as gpd
import os
import glob
import zipfile
from sqlalchemy import *
import pandas as pd


# Administrative models
class DRANEF(models.Model):
    id_dranef = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.name}"


class DPANEF(models.Model):
    id_dpanef = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    dranef = models.ForeignKey(DRANEF, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return f"{self.name}"


class ZDTF(models.Model):
    id_zdtf = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    dpanef = models.ForeignKey(DPANEF, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return f"{self.name}"


class DFP(models.Model):
    id_dfp = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    zdtf = models.ForeignKey(ZDTF, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return f"{self.name}"


# Regional models
class Region(models.Model):
    id_region = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    geometry = gis_model.PolygonField(srid=4326, null=True, blank=True)

    def __str__(self):
        return f"{self.name}"


class Province(models.Model):
    id_province = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    geometry = gis_model.PolygonField(srid=4326, null=True, blank=True)
    region = models.ForeignKey(Region, on_delete=models.CASCADE, null=True)
    

    def __str__(self):
        return f"{self.name}"


class Commune(models.Model):
    id_commune = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    geometry = gis_model.PolygonField(srid=4326, null=True, blank=True)
    province = models.ForeignKey(Province, on_delete=models.CASCADE, null=True)
    

    def __str__(self):
        return f"{self.name}"


# Forest models
class Forest(models.Model):
    id_forest = models.AutoField(primary_key=True)
    forest_name = models.CharField(max_length=255)
    loca_name = models.CharField(max_length=255)
    superficie = models.DecimalField(max_digits=12, decimal_places=3)
    geometry = gis_model.MultiPolygonField(srid=4326, null=True, blank=True)
    num_canton = models.IntegerField(null=True, blank=True)  # Allow NULL in DB
    num_parcel = models.IntegerField(null=True, blank=True)  # Allow NULL in DB
    titre_fonci = models.CharField(max_length=255, null=True, blank=True)
    for_formatio = models.CharField(max_length=255, null=True, blank=True)
    

    def __str__(self):
        return f"{self.forest_name}"


class Canton(models.Model):
    id_canton = models.AutoField(primary_key=True)
    canton_name = models.CharField(max_length=255)
    superficie = models.DecimalField(max_digits=12, decimal_places=3)
    geometry = gis_model.MultiPolygonField(srid=4326, null=True, blank=True)
    num_groupe = models.IntegerField(null=True, blank=True)  # Allow NULL in DB
    forest = models.ForeignKey(Forest, on_delete=models.CASCADE, null=True, blank=True)
    # properties=models.JSONField(default=True, blank=True)

    def __str__(self):
        return f"{self.canton_name}"


class Groupe(models.Model):
    id_groupe = models.AutoField(primary_key=True)
    groupe_name = models.CharField(max_length=255, null=True)
    superficie = models.DecimalField(max_digits=12, decimal_places=3)
    geometry = gis_model.MultiPolygonField(srid=4326, null=True, blank=True)
    parcel_num = models.IntegerField(null=True, blank=True)  # Allow NULL in DB
    forest = models.ForeignKey(Forest, on_delete=models.CASCADE, null=True, blank=True)
    canton = models.ForeignKey(Canton, on_delete=models.CASCADE, null=True, blank=True)
    
    class Meta:
        db_table = 'Groupe'
    

    def clean(self):
        if not self.canton and not self.forest:
            raise ValidationError("Groupe must be related to either a forest or a canton.")
        if self.canton and self.forest:
            raise ValidationError("Groupe cannot be related to both a canton and a forest.")

    def __str__(self):
        return f"{self.groupe_name}"
    


class Parcelle(models.Model):
    id_parcel = models.AutoField(primary_key=True)
    parcelle = models.CharField(max_length=255)
    superficie = models.DecimalField(max_digits=12, decimal_places=3)
    location = models.CharField(max_length=255, null=True, blank=True)
    groupe = models.ForeignKey(Groupe, on_delete=models.CASCADE, null=True, blank=True)
    geometry = gis_model.PolygonField(srid=4326, null=True, blank=True)
    commune = models.ForeignKey(Commune, on_delete=models.CASCADE, null=True, blank=True)
    dfp = models.ForeignKey(DFP, on_delete=models.CASCADE, null=True, blank=True)
    

    def __str__(self):
        return f"{self.parcelle}"
    
    class Meta:
        db_table = 'Parcelle'


class Species(models.Model):
    id_species = models.AutoField(primary_key=True)
    sci_name = models.CharField(max_length=255, blank=True)
    vernac_name = models.CharField(max_length=255, null=True, blank=True)
    french_name = models.CharField(max_length=255, null=True, blank=True)
    spp_decript = models.TextField()
    

    def __str__(self):
        scientific = self.sci_name
        return f"{scientific}"


class ParcelSpecies(models.Model):
    sci_name = models.ForeignKey(Species, on_delete=models.PROTECT)
    parcelle = models.ForeignKey(Parcelle, on_delete=models.PROTECT)
    num_species = models.IntegerField(null=True,blank=True)
    vol_total =models.FloatField(null=True,blank=True)
    num_total= models.IntegerField(null=True, blank=True)
    

    def __str__(self):
        nom_secientifique = self.sci_name or ""
        parcelle = self.parcelle or ""
        return f"{nom_secientifique}, {parcelle}"


# Model for the point cloud metadata
class PointCloudMetaData(models.Model):
    date_collec = models.DateField(null=True, blank=True, default=datetime.date.today)
    responsable = models.CharField(max_length=255, null=True, blank=True)
    id_parcelle = models.ForeignKey(Parcelle, on_delete=models.CASCADE, null=True, blank=True)
    threeD_mod = models.URLField(null=True, blank=True)
    

    # volume = models.FloatField(null=True, blank=True),
    # description = models.TextField(null=True, blank=True)

    # def calculate_volume(self):
    #     if self.circumference and self.height:
    #         radius = self.circumference / (2 * math.pi)
    #         self.volume = math.pi * (radius ** 2) * self.height
    #         return self.volume
    #     return None

    # def save(self, *args, **kwargs):
    #     # Automatically calculate volume before saving
    #     self.calculate_volume()
    #     super(PointCloudMetadata, self).save(*args, **kwargs)

class EspeceInventaire(models.Model):
    circonf = models.FloatField(null=True,blank=True)
    num_arbre = models.IntegerField(null=True,blank=True)
    hauteur=models.FloatField(null=True,blank=True)
    vol_arbre =models.FloatField(null=True,blank=True)
    id_parcespp = models.ForeignKey(ParcelSpecies,on_delete=models.CASCADE, null=True, blank=True)
    
    
conn_str = f"postgresql://postgres:{config('DB_PASSWORD')}@localhost:5432/{config('DB_NAME')}"
    

class Shp(models.Model):
    TARGET_MODELS = (
        ('parcelle', 'Parcelle'),
        ('canton', 'Canton'),
        ('groupe', 'Groupe'),
    )
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=1000, blank=True)
    file = models.FileField(upload_to='%Y/%m/%d')
    date = models.DateField(default=datetime.date.today, blank=True)
    model_type = models.CharField(max_length=10, choices=TARGET_MODELS)

    def __str__(self):
        return self.name

@receiver(post_save, sender=Shp)
def publish_data(sender, instance, created, **kwargs):
    if not instance.model_type:
        print("No target model specified for the shapefile upload.")
        return

    file = instance.file.path
    try:
        # Extract the shapefile
        with zipfile.ZipFile(file, 'r') as zip_ref:
            zip_ref.extractall(os.path.dirname(file))
        
        # Load the shapefile into a GeoDataFrame
        shp_path = glob.glob(os.path.join(os.path.dirname(file), '*.shp'))[0]
        gdf = gpd.read_file(shp_path)

        # Determine the target model dynamically
        target_model_map = {
            'parcelle': 'parcelle',
            'canton': 'canton',
            'groupe': 'groupe',
        }
        target_table = target_model_map.get(instance.model_type)

        if not target_table:
            raise ValueError(f"Invalid model type: {instance.model_type}")

        # Save the GeoDataFrame to the target table in the database
        engine = create_engine(conn_str)
        gdf.to_postgis(
            name=target_table,
            con=engine,
            if_exists='append',
            index=False
        )

        # Clean up extracted files
        for extracted_file in glob.glob(os.path.join(os.path.dirname(file), '*')):
            os.remove(extracted_file)

    except Exception as e:
        print(f"Error processing shapefile: {e}")

    
# class ShapefileUpload(models.Model):
#     name = models.CharField(max_length=255)
#     shapefile = models.FileField(upload_to="shapefiles/")  # Save .shp files
#     uploaded_at = models.DateTimeField(auto_now_add=True)
#     model_name = models.CharField(max_length=255, help_text="Enter the target model name (e.g Parcelle).",default="defaultModelName")

#     def __str__(self):
#         return f"Shapefile uploaded on {self.uploaded_at}" or f"{self.name}"


