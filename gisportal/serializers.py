from rest_framework import serializers
from django.db import models
from django_filters import CharFilter   
from rest_framework_gis.serializers import GeoFeatureModelSerializer
from gisportal.models import (
    DRANEF, DPANEF, ZDTF, DFP, Region, Province, Commune, Forest,
    Canton, Groupe, Parcelle, Species, ParcelSpecies,PointCloudMetaData)

# Standard serializers for non-spatial models
class DRANEFSerializer(serializers.ModelSerializer):
    class Meta:
        model = DRANEF
        fields = '__all__'
    

class DPANEFSerializer(serializers.ModelSerializer):
    dranef = DRANEFSerializer(read_only=True)
    class Meta:
        model = DPANEF
        fields = '__all__'


class ZDTFSerializer(serializers.ModelSerializer):
    dpnef = DPANEFSerializer(read_only=True)
    class Meta:
        model = ZDTF
        fields = '__all__'


class DFPSerializer(serializers.ModelSerializer):
    zdtf = ZDTFSerializer(read_only=True)
    class Meta:
        model = DFP
        fields = '__all__'


class RegionSerializer(serializers.ModelSerializer):
    # Removed 'dpf' as it doesn't appear to be a field in Region
    class Meta:
        model = Region
        fields = '__all__'


class ProvinceSerializer(serializers.ModelSerializer):
    region = RegionSerializer(read_only=True)
    class Meta:
        model = Province
        fields = '__all__'


class CommuneSerializer(serializers.ModelSerializer):
    province = ProvinceSerializer(read_only=True)
    class Meta:
        model = Commune
        fields = '__all__'


# GeoJSON-compatible serializers for spatial models
class ForestSerializer(GeoFeatureModelSerializer):
    class Meta:
        model = Forest
        geo_field = "geom" 
        fields = ('id_forest', 'forest_name', 'location_name', 'surface_area','number_canton', 'number_parcel', 'titre_foncier', 'forest_formation')
        
    
class CantonSerializer(GeoFeatureModelSerializer):
    class Meta:
        model = Canton
        geo_field = "geom"
        fields = ('id_canton', 'canton_name', 'surface_area', 'number_groupe','forest')


class GroupeSerializer(GeoFeatureModelSerializer):
    class Meta:
        model = Groupe
        geo_field = "geom"
        fields = ('id_groupe', 'groupe_name', 'surface_area', 'parcel_number', 'forest', 'canton')


class ParcelleSerializer(GeoFeatureModelSerializer):
    class Meta:
        model = Parcelle
        geo_field = "geom"
        fields = ('id_parcelle', 'parcelle_name', 'surface_area', 'location', 'groupe', 'commune', 'dfp')


class SpeciesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Species
        #geo_field = "geom"
        fields =('id_species', 'scientific_name', 'vernacular_name', 'french_name', 'species_importance')


class ParcelSpeciesSerializer(serializers.ModelSerializer):
    # Nested representation of related Species and Parcelle models
    species = SpeciesSerializer(read_only=True)
    parcelle = ParcelleSerializer(read_only=True)

    class Meta:
        model = ParcelSpecies
        fields = ('species', 'parcelle','num_species')
        
        
class PointCloudMetaDataSerializer(serializers.ModelSerializer):
    class Meta:
        model:PointCloudMetaData
        fields = ['object_id', 'species', 'height','circuference ','more_fields','description'] 

        
    
#cesium ion serialization
class CesiumIonAssetSerializer(serializers.Serializer):
    asset_id = serializers.IntegerField()
    access_token = serializers.CharField()
    
     



    