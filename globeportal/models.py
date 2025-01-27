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
from sqlalchemy import create_engine
import pandas as pd # type: ignore


# Administrative models
class DRANEF(models.Model):
    id_dranef = models.AutoField(primary_key=True, db_column='id_dranef')
    name = models.CharField(max_length=255, db_column='name')

    def __str__(self):
        return f"{self.name}"


class DPANEF(models.Model):
    id_dpanef = models.AutoField(primary_key=True, db_column='id_dpanef')
    name = models.CharField(max_length=255, db_column='name')
    dranef = models.ForeignKey(DRANEF, on_delete=models.CASCADE, null=True, db_column='dranef')

    def __str__(self):
        return f"{self.name}"


class ZDTF(models.Model):
    id_zdtf = models.AutoField(primary_key=True, db_column='id_zdtf')
    name = models.CharField(max_length=255, db_column='name')
    dpanef = models.ForeignKey(DPANEF, on_delete=models.CASCADE, null=True, db_column='dpanef')

    def __str__(self):
        return f"{self.name}"


class DFP(models.Model):
    id_dfp = models.AutoField(primary_key=True, db_column='id_dfp')
    name = models.CharField(max_length=255, db_column='name')
    zdtf = models.ForeignKey(ZDTF, on_delete=models.CASCADE, null=True, db_column='zdtf')

    def __str__(self):
        return f"{self.name}"


# Regional models
class Region(models.Model):
    id_region = models.AutoField(primary_key=True, db_column='id_region')
    name = models.CharField(max_length=255, db_column='name')
    superficie = models.DecimalField(max_digits=12, decimal_places=3, null=True, blank=True, db_column='superficie')
    geometry = gis_model.PolygonField(srid=4326, null=True, blank=True, db_column='geometry')

    def __str__(self):
        return f"{self.name}"


class Province(models.Model):
    id_provinc = models.AutoField(primary_key=True, db_column='id_provinc')
    name = models.CharField(max_length=255, db_column='name')
    superficie = models.DecimalField(max_digits=12, decimal_places=3, null=True, blank=True, db_column='superficie')
    geometry = gis_model.PolygonField(srid=4326, null=True, blank=True, db_column='geometry')
    region = models.ForeignKey(Region, on_delete=models.CASCADE, null=True, db_column='region')

    def __str__(self):
        return f"{self.name}"


class Commune(models.Model):
    id_commune = models.AutoField(primary_key=True, db_column='id_commune')
    name = models.CharField(max_length=255, db_column='name')
    geometry = gis_model.PolygonField(srid=4326, null=True, blank=True, db_column='geometry')
    province_i = models.ForeignKey(Province, on_delete=models.CASCADE, null=True, db_column='province_i')
    superficie = models.DecimalField(max_digits=12, decimal_places=3, null=True, blank=True, db_column='superficie')

    def __str__(self):
        return f"{self.name}"


# Forest models
class Forest(models.Model):
    id_forest = models.AutoField(primary_key=True, db_column='id_forest')
    forest_nam = models.CharField(max_length=255, db_column='forest_nam')
    loc_name = models.CharField(max_length=255, db_column='loc_name')
    superficie = models.DecimalField(max_digits=12, decimal_places=3, db_column='superficie')
    geometry = gis_model.MultiPolygonField(srid=4326, null=True, blank=True, db_column='geometry')
    num_canton = models.IntegerField(null=True, blank=True, db_column='num_canton')  # Allow NULL in DB
    num_parcel = models.IntegerField(null=True, blank=True, db_column='num_parcel')  # Allow NULL in DB
    titre_fonc = models.CharField(max_length=255, null=True, blank=True, db_column='titre_fonc')
    for_format = models.CharField(max_length=255, null=True, blank=True, db_column='for_format')

    def __str__(self):
        return f"{self.forest_nam}"


class Canton(models.Model):
    id_canton = models.AutoField(primary_key=True, db_column='id_canton')
    canton_nam = models.CharField(max_length=255, db_column='canton_nam')
    superficie = models.DecimalField(max_digits=12, decimal_places=3, db_column='superficie')
    geometry = gis_model.MultiPolygonField(srid=4326, null=True, blank=True, db_column='geometry')
    num_groupe = models.IntegerField(null=True, blank=True, db_column='num_groupe')  # Allow NULL in DB
    forest_id = models.ForeignKey(Forest, on_delete=models.CASCADE, null=True, blank=True, db_column='forest_id')

    def __str__(self):
        return f"{self.canton_nam}"


class Groupe(models.Model):
    id_groupe = models.AutoField(primary_key=True, db_column='id_groupe')
    groupe_name = models.CharField(max_length=255, null=True, db_column='groupe_name')
    superficie = models.DecimalField(max_digits=12, decimal_places=3, db_column='superficie')
    geometry = gis_model.MultiPolygonField(srid=4326, null=True, blank=True, db_column='geometry')
    parcel_num = models.IntegerField(null=True, blank=True, db_column='parcel_num')  # Allow NULL in DB
    forest = models.ForeignKey(Forest, on_delete=models.CASCADE, null=True, blank=True, db_column='forest')
    canton = models.ForeignKey(Canton, on_delete=models.CASCADE, null=True, blank=True, db_column='canton')

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
    superficie = models.DecimalField(max_digits=12, decimal_places=3, null=True, blank=True, db_column='superficie')
    geometry = gis_model.PolygonField(srid=4326, null=True, blank=True, db_column='geometry')
    commune_id = models.ForeignKey(Commune, on_delete=models.CASCADE, null=True, blank=True, db_column='commune_id')
    dfp_id = models.ForeignKey(DFP, on_delete=models.CASCADE, null=True, blank=True, db_column='dfp_id')
    location = models.CharField(max_length=255, null=True, blank=True, db_column='location')
    groupe_id = models.ForeignKey(Groupe, on_delete=models.CASCADE, null=True, blank=True, db_column='groupe_id')

    def __str__(self):
        return f"{self.parcelle}"


class Species(models.Model):
    id_species = models.AutoField(primary_key=True, db_column='id_species')
    sci_name = models.CharField(max_length=255, blank=True, db_column='sci_name')
    vernac_name = models.CharField(max_length=255, null=True, blank=True, db_column='vernac_name')
    french_name = models.CharField(max_length=255, null=True, blank=True, db_column='french_name')
    spp_descript = models.TextField(null=True, blank=True, db_column='spp_descript')

    def __str__(self):
        scientific = self.sci_name
        return f"{scientific}"


class ParcelSpecies(models.Model):
    sci_name = models.ForeignKey(Species, on_delete=models.PROTECT, db_column='sci_name')    
    parcelle = models.ForeignKey(Parcelle, on_delete=models.PROTECT, db_column='parcelle')
    num_species = models.IntegerField(null=True, blank=True, db_column='num_species')
    vol_total = models.FloatField(null=True, blank=True, db_column='vol_total')
    num_total = models.IntegerField(null=True, blank=True, db_column='num_total')

    def __str__(self):
        nom_secientifique = self.sci_name or ""
        parcelle = self.parcelle or ""
        return f"{nom_secientifique}, {parcelle}"


# Model for the point cloud metadata
class PointCloudMetaData(models.Model):
    date = models.DateField(null=True, blank=True, default=datetime.date.today, db_column='date')
    responsable = models.CharField(max_length=255, null=True, blank=True, db_column='responsable')
    id_parcel = models.ForeignKey(Parcelle, on_delete=models.CASCADE, null=True, blank=True, db_column='id_parcel')
    threeD_mod = models.URLField(null=True, blank=True, db_column='threeD_mod')

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
    circonf = models.FloatField(null=True, blank=True, db_column='circonf')
    num_arbre = models.IntegerField(null=True, blank=True, db_column='num_arbre')
    hauteur = models.FloatField(null=True, blank=True, db_column='hauteur')
    vol_arbre = models.FloatField(null=True, blank=True, db_column='vol_arbre')
    id_parcspp = models.ForeignKey(ParcelSpecies, on_delete=models.CASCADE, null=True, blank=True, db_column='id_parcspp')


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
    if created:
        file = instance.file.path
        file_format = os.path.basename(file).split('.')[-1]
        file_name = os.path.basename(file).split('.')[0]
        file_path = os.path.dirname(file)
        name = instance.name

        try:
            # Extract the ZIP file
            with zipfile.ZipFile(file, 'r') as zip_ref:
                zip_ref.extractall(file_path)
            os.remove(file)  # Remove the original ZIP file

            shp = glob.glob(r'{}/**/*.shp'.format(file_path), recursive=True)  # Find SHP files
            req_shp = shp[0]
            gdf = gpd.read_file(req_shp)  # Load SHP into a GeoDataFrame

            if gdf.crs is None:
                gdf.set_crs("EPSG:4326", inplace=True)
            else:
                gdf = gdf.to_crs("EPSG:4326")

            engine = create_engine(conn_str)

            if name == 'portal_parcelle':
                with engine.connect() as conn:
                    valid_groupe_ids = pd.read_sql('SELECT id_groupe FROM "public"."groupe"', conn)['id_groupe'].tolist()
                    valid_commune_ids = pd.read_sql('SELECT id_commune FROM "public"."portal_commune"', conn)['id_commune'].tolist()
                    valid_dfp_ids = pd.read_sql('SELECT id_dfp FROM "public"."portal_dfp"', conn)['id_dfp'].tolist()

                if 'groupe_id' in gdf.columns:
                    gdf = gdf[(gdf['groupe_id'].isnull()) | (gdf['groupe_id'].isin(valid_groupe_ids))]

                if 'commune_id' in gdf.columns:
                    gdf = gdf[(gdf['commune_id'].isnull()) | (gdf['commune_id'].isin(valid_commune_ids))]

                if 'dfp_id' in gdf.columns:
                    gdf = gdf[(gdf['dfp_id'].isnull()) | (gdf['dfp_id'].isin(valid_dfp_ids))]

            elif name == 'portal_groupe':
                with engine.connect() as conn:
                    valid_forest_ids = pd.read_sql('SELECT id_forest FROM "public"."portal_forest"', conn)['id_forest'].tolist()
                    valid_canton_ids = pd.read_sql('SELECT id_canton FROM "public"."portal_canton"', conn)['id_canton'].tolist()

                if 'forest_id' in gdf.columns:
                    gdf = gdf[(gdf['forest_id'].isnull()) | (gdf['forest_id'].isin(valid_forest_ids))]

                if 'canton_id' in gdf.columns:
                    gdf = gdf[(gdf['canton_id'].isnull()) | (gdf['canton_id'].isin(valid_canton_ids))]

            elif name == 'portal_canton':
                with engine.connect() as conn:
                    valid_forest_ids = pd.read_sql('SELECT id_forest FROM "public"."portal_forest"', conn)['id_forest'].tolist()

                if 'forest_id' in gdf.columns:
                    gdf = gdf[(gdf['forest_id'].isnull()) | (gdf['forest_id'].isin(valid_forest_ids))]

            elif name == 'portal_forest':
                pass

            elif name == 'portal_commune':
                with engine.connect() as conn:
                    valid_province_ids = pd.read_sql('SELECT id_provinc FROM "public"."portal_province"', conn)['id_provinc'].tolist()

                if 'province_i' in gdf.columns:
                    gdf = gdf[(gdf['province_i'].isnull()) | (gdf['province_i'].isin(valid_province_ids))]

            elif name == 'portal_province':
                with engine.connect() as conn:
                    valid_region_ids = pd.read_sql('SELECT id_region FROM "public"."portal_region"', conn)['id_region'].tolist()

                if 'region_id' in gdf.columns:
                    gdf = gdf[(gdf['region_id'].isnull()) | (gdf['region_id'].isin(valid_region_ids))]

            elif name == 'portal_region':
                pass

            else:
                pass

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

            instance.delete()  # Delete the instance if an error occurs
            print("There is a problem during shp upload: ", e)
