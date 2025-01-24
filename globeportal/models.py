from django.db import models  # type: ignore
from django.contrib.gis.gdal import DataSource  # type: ignore
from django.contrib.gis.geos import GEOSGeometry  # type: ignore
from django.contrib.gis.db import models as gis_model  # type: ignore
from django.core.exceptions import ValidationError  
import datetime
# from decouple import config

from django.db.models.signals import post_save
from django.dispatch import receiver
import geopandas as gpd
import os
import glob
import zipfile
from sqlalchemy import *
from sqlalchemy.sql import text 
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
    loc_name = models.CharField(max_length=255)
    superficie = models.DecimalField(max_digits=12, decimal_places=3)
    geometry = gis_model.MultiPolygonField(srid=4326, null=True, blank=True)
    num_canton = models.IntegerField(null=True, blank=True)  # Allow NULL in DB
    num_parcel = models.IntegerField(null=True, blank=True)  # Allow NULL in DB
    titre_fonci = models.CharField(max_length=255, null=True, blank=True)
    for_format = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return f"{self.forest_name}"


class Canton(models.Model):
    id_canton = models.AutoField(primary_key=True)
    canton_name = models.CharField(max_length=255)
    superficie = models.DecimalField(max_digits=12, decimal_places=3)
    geometry = gis_model.MultiPolygonField(srid=4326, null=True, blank=True)
    number_groupe = models.IntegerField(null=True, blank=True)  # Allow NULL in DB
    forest = models.ForeignKey(Forest, on_delete=models.CASCADE, null=True, blank=True)

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

    
    def clean(self):
        if not self.canton and not self.forest:
            raise ValidationError("Groupe must be related to either a forest or a canton.")
        if self.canton and self.forest:
            raise ValidationError("Groupe cannot be related to both a canton and a forest.")

    def __str__(self):
        return f"{self.groupe_name}"
    
    class Meta:
        db_table = 'groupe'


class Parcelle(models.Model):
    id_parcel = models.AutoField(primary_key=True, db_column='id_parcel')
    parcelle = models.CharField(max_length=255, db_column='parcelle')
    superficie = models.DecimalField(max_digits=12, decimal_places=3, null=True, blank=True,db_column='superficie')
    geometry = gis_model.PolygonField(srid=4326, null=True, blank=True, db_column='geometry')
    commune_id = models.ForeignKey(Commune, on_delete=models.CASCADE, null=True, blank=True, db_column='commune_id')
    dfp_id = models.ForeignKey(DFP, on_delete=models.CASCADE, null=True, blank=True, db_column='dfp_id')
    location = models.CharField(max_length=255, null=True, blank=True, db_column='location')
    groupe_id = models.ForeignKey(Groupe, on_delete=models.CASCADE, null=True, blank=True, db_column='groupe_id')

    def __str__(self):
        return f"{self.parcelle}"


class Species(models.Model):
    id_species = models.AutoField(primary_key=True)
    sci_name = models.CharField(max_length=255, blank=True)
    vernac_name = models.CharField(max_length=255, null=True, blank=True)
    french_name = models.CharField(max_length=255, null=True, blank=True)
    spp_descript = models.TextField()

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
    date = models.DateField(null=True, blank=True, default=datetime.date.today)
    responsable = models.CharField(max_length=255, null=True, blank=True)
    id_parcel = models.ForeignKey(Parcelle, on_delete=models.CASCADE, null=True, blank=True)
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
    id_parcspp = models.ForeignKey(ParcelSpecies,on_delete=models.CASCADE, null=True, blank=True)
    


class ShapefileUpload(models.Model):
    name = models.CharField(max_length=255)
    shapefile = models.FileField(upload_to="shapefiles/")  # Save .shp files
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name}"
    

conn_str = "postgresql://postgres:1114@localhost:5432/portal"
    

class Shpss(models.Model):
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=1000, blank=True)
    file = models.FileField(upload_to='%Y/%m/%d')
    date = models.DateField(default=datetime.date.today, blank=True)
    
    def __str__(self):
        return f"{self.name}"

@receiver(post_save, sender=Shpss)
def publish_data(sender, instance, created, **kwargs):
    file = instance.file.path
    file_format = os.path.basename(file).split('.')[-1]
    file_name = os.path.basename(file).split('.')[0]
    file_path = os.path.dirname(file)
    name = instance.name

    # Extraire le fichier ZIP
    with zipfile.ZipFile(file, 'r') as zip_ref:
        zip_ref.extractall(file_path)
    os.remove(file)  # Supprimer le fichier ZIP d'origine

    shp = glob.glob(r'{}/**/*.shp'.format(file_path), recursive=True)  # Trouver les fichiers SHP
    try:
        req_shp = shp[0]
        gdf = gpd.read_file(req_shp)  # Charger le SHP dans un GeoDataFrame

        if gdf.crs is None:
            gdf.set_crs("EPSG:4326", inplace=True)
        else:
            gdf = gdf.to_crs("EPSG:4326")
            
        engine = create_engine(conn_str)

        if name=='portal_parcelle':

            with engine.connect() as conn:
                # Récupérer les ID valides des deux tables
                valid_groupe_ids = pd.read_sql('SELECT id_groupe FROM "public"."groupe"', conn)['id_groupe'].tolist()
                valid_commune_ids = pd.read_sql('SELECT id_commune FROM "public"."portal_commune"', conn)['id_commune'].tolist()
                valid_dfp_ids= pd.read_sql('SELECT id_dfp FROM "public"."portal_dfp"', conn)['id_dfp'].tolist()

            # Filtrer les données pour correspondre aux deux clés étrangères
            # Si la colonne est nulle, aucun filtre n'est appliqué pour cette clé
            if 'groupe_id' in gdf.columns:
                gdf = gdf[(gdf['groupe_id'].isnull()) | (gdf['groupe_id'].isin(valid_groupe_ids))]

            if 'commune_id' in gdf.columns:
                gdf = gdf[(gdf['commune_id'].isnull()) | (gdf['commune_id'].isin(valid_commune_ids))]
                
            if 'dfp_id' in gdf.columns:
                gdf = gdf[(gdf['dfp_id'].isnull()) | (gdf['dfp_id'].isin(valid_dfp_ids))]
        
        else:
            pass

        # Insérer dans PostgreSQL
        gdf.to_postgis(
            con=engine,
            schema='public',
            name=name,
            if_exists="append"
        )

        for s in shp:
            os.remove(s)

    except Exception as e:
        for s in shp:
            os.remove(s)

        instance.delete()  # Supprimer l'instance si une erreur survient
        print("There is a problem during shp upload: ", e)