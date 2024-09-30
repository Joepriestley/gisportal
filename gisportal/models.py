from django.db import models # type: ignore
from django.contrib.gis.db import models as gismodel # type: ignore
from django.core.exceptions import ValidationError # type: ignore


# Administrative models
class DRANEF(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.name}"

class DPANEF(models.Model):
    name = models.CharField(max_length=255)
    dranef = models.ForeignKey(DRANEF, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return f"{self.name}"


class ZDTF(models.Model):
    name = models.CharField(max_length=255)
    dpanef = models.ForeignKey(DPANEF, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return f"{self.name}"


class DFP(models.Model):
    name = models.CharField(max_length=255)
    zdtf = models.ForeignKey(ZDTF, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return f"{self.name}"


# Regional models
class Region(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.name}"


class Province(models.Model):
    name = models.CharField(max_length=255)
    region = models.ForeignKey(Region, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return f"{self.name}"

class Commune(models.Model):
    name = models.CharField(max_length=255)
    province = models.ForeignKey(Province, on_delete=models.CASCADE,null=True)

    def __str__(self):
        return f"{self.name}"


# Forest models
class Forest(models.Model):
    FORMATION_RESINEUSES = 'R'
    FORMATION_FEUILLEUSES = 'F'
    FORMATION_CEDRAIES = 'C'
    FORMATION_SUBERAIES = 'S'
    FORMATION_PINEDES = 'P'

    FORMATION_CHOICES = [
        (FORMATION_RESINEUSES, 'LES RESINEUSES'),
        (FORMATION_FEUILLEUSES, 'LES FEUILLEUSES'),
        (FORMATION_CEDRAIES, 'LES CEDRAIES'),
        (FORMATION_SUBERAIES, 'LES SUBERAIES'),
        (FORMATION_PINEDES, 'LES PINEDES'),
    ]

    forest_name = models.CharField(max_length=255)
    location_name = models.CharField(max_length=255)
    surface_area = models.DecimalField(max_digits=7, decimal_places=3)
    geom = gismodel.MultiPolygonField(srid=4326, null=True)
    num_canton = models.IntegerField(blank=True)
    number_parcel = models.IntegerField(blank=True)
    titre_foncier = models.CharField(max_length=255, null=True, blank=True)
    forest_formation = models.CharField(max_length=1, choices=FORMATION_CHOICES, default=FORMATION_FEUILLEUSES)

    def __str__(self):
        return f"{self.forest_name}, {self.location_name}"


class Canton(models.Model):
    canton_name = models.CharField(max_length=255)
    surface_area = models.DecimalField(max_digits=6, decimal_places=3)
    geom = gismodel.MultiPolygonField(srid=4326, null=True)
    num_groupe = models.IntegerField(blank=True)
    forest = models.ForeignKey(Forest, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return f"{self.canton_name}"


class Groupe(models.Model):
    groupe_name = models.CharField(max_length=255, null=True)
    surface_area = models.DecimalField(max_digits=6, decimal_places=3)
    geom = gismodel.MultiPolygonField(srid=4326, null=True)
    parcel_number = models.IntegerField(blank=True)
    forest = models.ForeignKey(Forest, on_delete=models.CASCADE, null=True, blank=True)
    canton = models.ForeignKey(Canton, on_delete=models.CASCADE, null=True, blank=True)

    # Validation to ensure that Groupe is related to either a forest or a canton, not both
    def clean(self):
        if not self.canton and not self.forest:
            raise ValidationError("Groupe must be related to either a forest or a canton.")
        if self.canton and self.forest:
            raise ValidationError("Groupe cannot be related to both a canton and a forest.")

    def __str__(self):
        return f"{self.groupe_name}"


class Parcelle(models.Model):
    parcelle_name = models.CharField(max_length=255)
    surface_area = models.DecimalField(max_digits=6, decimal_places=3)
    location = models.CharField(max_length=255, null=True, blank=True)
    groupe = models.ForeignKey(Groupe, on_delete=models.CASCADE, null=True, blank=True)
    commune = models.ForeignKey(Commune, on_delete=models.CASCADE, null=True, blank=True)
    dfp = models.ForeignKey(DFP, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return f"{self.parcelle_name}"


# Species and relation models
class Species(models.Model):
    scientific_name = models.CharField(max_length=255, primary_key=True, blank=True)
    vernacular_name = models.CharField(max_length=255, null=True, blank=True)
    french_name = models.CharField(max_length=255, null=True, blank=True)
    geom = gismodel.PointField(srid=4326, null=True)
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

    def __str__(self):
        return f"{self.scientific_name}"