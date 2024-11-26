# serializers.py
from rest_framework import serializers
from rest_framework_gis.serializers import GeoFeatureModelSerializer
from gisportal.models import (
DRANEF, DPANEF, ZDTF, DFP, Region, Province, Commune, Forest,
Canton, Groupe, Parcelle, Species, ParcelSpecies
)

# DRANEF Serializer
class DRANEFSerializer(serializers.ModelSerializer):
    class Meta:
        model = DRANEF
        fields = ['id_dranef', 'name']

# DPANEF Serializer (Nested with DRANEF)
class DPANEFSerializer(serializers.ModelSerializer):
    dranef = DRANEFSerializer(read_only=True)

    class Meta:
        model = DPANEF
        fields = ['id_dpanef', 'name', 'dranef']

# ZDTF Serializer (Nested with DPANEF)
class ZDTFSerializer(serializers.ModelSerializer):
    dpanef = DPANEFSerializer(read_only=True)

    class Meta:
        model = ZDTF
        fields = ['id_zdtf', 'name', 'dpanef']
        
class DFPSerializer(serializers.ModelSerializer):
    zdtf =ZDTFSerializer(read_only=True)
    class Meta:
        model =DFP
        fields =['id_dfp','name','zdtf']

# Region Serializer
class RegionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Region
        fields = ['id_region', 'name']

# Province Serializer (Nested with Region)
class ProvinceSerializer(serializers.ModelSerializer):
    region = RegionSerializer(read_only=True)

    class Meta:
        model = Province
        fields = ['id_province', 'name', 'region']

# Commune Serializer (Nested with Province)
class CommuneSerializer(serializers.ModelSerializer):
    province = ProvinceSerializer(read_only=True)

    class Meta:
        model = Commune
        fields = ['id_commune', 'name', 'province']

# Forest Serializer
class ForestSerializer(serializers.ModelSerializer):
    class Meta:
        model = Forest
        fields = [
            'id_forest', 'forest_name', 'location_name', 'surface_area', 'geom',
            'num_canton', 'number_parcel', 'titre_foncier', 'forest_formation'
        ]

# Canton Serializer (Nested with Forest)
class CantonSerializer(serializers.ModelSerializer):
    forest = ForestSerializer(read_only=True)

    class Meta:
        model = Canton
        fields = ['id_canton', 'canton_name', 'surface_area', 'geom', 'num_groupe', 'forest']

# Groupe Serializer (Nested with Forest and Canton)
class GroupeSerializer(serializers.ModelSerializer):
    forest = ForestSerializer(read_only=True)
    canton = CantonSerializer(read_only=True)

    class Meta:
        model = Groupe
        fields = ['id_groupe', 'groupe_name', 'surface_area', 'geom', 'parcel_number', 'forest', 'canton']

# Parcelle Serializer (Nested with Groupe, Commune, and DFP)
class ParcelleSerializer(serializers.ModelSerializer):
    groupe = GroupeSerializer(read_only=True)
    commune = CommuneSerializer(read_only=True)
    dfp = ZDTFSerializer(read_only=True)

    class Meta:
        model = Parcelle
        fields = [
            'id_parcelle', 'parcelle_name', 'surface_area', 'location', 'groupe', 'commune', 'dfp'
        ]

# Species Serializer
class SpeciesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Species
        fields = [
            'id_groupe', 'scientific_name', 'vernacular_name', 'french_name',
            'geom', 'species_importance'
        ]

# ParcelSpecies Serializer (Nested with Species and Parcelle)
class ParcelSpeciesSerializer(serializers.ModelSerializer):
    scientific_name = SpeciesSerializer(read_only=True)
    parcelle = ParcelleSerializer(read_only=True)

    class Meta:
        model = ParcelSpecies
        fields = ['scientific_name', 'parcelle', 'num_species']
