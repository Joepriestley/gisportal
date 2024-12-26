from django.db import models # type: ignore
from django.contrib.gis.db import models as gis_model # type: ignore
from django.core.exceptions import ValidationError # type: ignore


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

    def __str__(self):
        return f"{self.name}"


class Province(models.Model):
    id_province = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    region = models.ForeignKey(Region, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return f"{self.name}"


class Commune(models.Model):
    id_commune = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    province = models.ForeignKey(Province, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return f"{self.name}"


# Forest models
class Forest(models.Model):
    FORMATION_CHOICES = [
        ('R', 'LES RESINEUSES'),
        ('F', 'LES FEUILLEUSES'),
        ('C', 'LES CEDRAIES'),
        ('S', 'LES SUBERAIES'),
        ('P', 'LES PINEDES'),
    ]

    id_forest = models.AutoField(primary_key=True)
    forest_name = models.CharField(max_length=255)
    location_name = models.CharField(max_length=255)
    surface_area = models.DecimalField(max_digits=12, decimal_places=3)
    geom = gis_model.MultiPolygonField(srid=4326, null=True, blank=True)
    num_canton = models.IntegerField(null=True, blank=True)  # Allow NULL in DB
    number_parcel = models.IntegerField(null=True, blank=True)  # Allow NULL in DB
    titre_foncier = models.CharField(max_length=255, null=True, blank=True)
    forest_formation = models.CharField(max_length=1, choices=FORMATION_CHOICES, default='F')

    def __str__(self):
        return f"{self.forest_name}, {self.location_name}"


class Canton(models.Model):
    id_canton = models.AutoField(primary_key=True)
    canton_name = models.CharField(max_length=255)
    surface_area = models.DecimalField(max_digits=6, decimal_places=3)
    geom = gis_model.MultiPolygonField(srid=4326, null=True, blank=True)
    num_groupe = models.IntegerField(null=True, blank=True)  # Allow NULL in DB
    forest = models.ForeignKey(Forest, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return f"{self.canton_name}"


class Groupe(models.Model):
    id_groupe = models.AutoField(primary_key=True)
    groupe_name = models.CharField(max_length=255, null=True)
    surface_area = models.DecimalField(max_digits=6, decimal_places=3)
    geom = gis_model.MultiPolygonField(srid=4326, null=True, blank=True)
    parcel_number = models.IntegerField(null=True, blank=True)  # Allow NULL in DB
    forest = models.ForeignKey(Forest, on_delete=models.CASCADE, null=True, blank=True)
    canton = models.ForeignKey(Canton, on_delete=models.CASCADE, null=True, blank=True)


    def clean(self):
        if not self.canton and not self.forest:
            raise ValidationError("Groupe must be related to either a forest or a canton.")
        if self.canton and self.forest:
            raise ValidationError("Groupe cannot be related to both a canton and a forest.")

    def __str__(self):
        return f"{self.groupe_name}"


class Parcelle(models.Model):
    id_parcelle = models.AutoField(primary_key=True)
    parcelle_name = models.CharField(max_length=255)
    surface_area = models.DecimalField(max_digits=6,decimal_places=3)
    location = models.CharField(max_length=255, null=True,blank=True)
    groupe = models.ForeignKey(Groupe, on_delete=models.CASCADE,null=True, blank=True)
    geom =gis_model.PolygonField(srid=4326,null=True, blank=True)
    commune = models.ForeignKey(Commune, on_delete=models.CASCADE,null=True, blank=True)
    dfp = models.ForeignKey(DFP, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return f"{self.parcelle_name}"


class Species(models.Model):
    id_species = models.AutoField(primary_key=True)
    scientific_name = models.CharField(max_length=255, blank=True)
    vernacular_name = models.CharField(max_length=255, null=True, blank=True)
    french_name = models.CharField(max_length=255, null=True, blank=True)
    # geom = gis_model.PointField(srid=4326, null=True, blank=True)
    species_importance = models.TextField()

    def __str__(self):
        vernacular = self.vernacular_name or ""
        french = self.french_name or ""
        scientific = self.scientific_name or ""
        return f"{vernacular}, {french}, {scientific}"


class ParcelSpecies(models.Model):
    scientific_name = models.ForeignKey(Species, on_delete=models.PROTECT)
    parcelle = models.ForeignKey(Parcelle, on_delete=models.PROTECT)
    num_species = models.IntegerField()
    num_total = models.IntegerField()
    volume_total = models.DecimalField(max_digits=7, decimal_places=3, null=True, blank=True)

    def __str__(self):
        nom_secientifique = self.scientific_name or ""
        parcelle = self.parcelle or ""
        return f"{nom_secientifique}, {parcelle}"

#model for the point cloud metadata 
class PointCloudMetaData(models.Model):
    object_id = models.IntegerField(unique=True,primary_key=True)
    species = models.CharField(max_length= 225, null=True,blank=True)
    height = models.FloatField()
    circuference =models.FloatField()
    #volume = models.FloatField(null=True, blank=True),
    more_fields = models.JSONField(null=True, blank=True)
    description = models.TextField(null=True,blank=True)
    
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

    
    def __str__(self):
        return f"object {self.object_id}:{self.species if self.species else 'unknown'}" 
    
class EspeceInventaire(models.Model):
    circonference = models.FloatField()
    num_total_arbre= models.IntegerField()
    hauteur = models.FloatField()
    volume_total_arbre = models.DecimalField(max_digits=7, decimal_places=3, null=True, blank=True)
    id_parcelspecies = models.ForeignKey(ParcelSpecies, on_delete=models.CASCADE)
         