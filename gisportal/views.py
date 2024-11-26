from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response 
from rest_framework import generics, status 
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from gisportal.models import (DRANEF,DPANEF,ZDTF,DFP,Region, Province, Commune, Forest, Canton, Groupe, Parcelle,Species,ParcelSpecies,PointCloudMetaData)

from gisportal.serializers import (DRANEFSerializer,DPANEFSerializer,ZDTFSerializer,DFPSerializer,RegionSerializer, ProvinceSerializer, CommuneSerializer, ForestSerializer, CantonSerializer, GroupeSerializer, ParcelleSerializer,SpeciesSerializer,ParcelSpeciesSerializer,PointCloudMetaDataSerializer)
from rest_framework.views import APIView
from gisportal.pagination import LargeResultsSetPagination


# Serialization
class DRANEFList(generics.ListCreateAPIView):
    queryset= DRANEF.objects.all()
    serializer_class =DRANEFSerializer
    filter_backends =[DjangoFilterBackend]
    filterset_fields =['name']

class DRANEFDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset =DRANEF.objects.all()
    serializer_class = DRANEFSerializer
    
class DPANEFList(generics.ListCreateAPIView):
    queryset= DPANEF.objects.all()
    serializer_class =DPANEFSerializer
    filter_backends =[DjangoFilterBackend]
    filterset_fields =['name']

class DPANEFDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset =DPANEF.objects.all()
    serializer_class = DPANEFSerializer
    
class ZDTFList(generics.ListCreateAPIView):
    queryset= ZDTF.objects.all()
    serializer_class =ZDTFSerializer
    filter_backends =[DjangoFilterBackend]
    filterset_fields =['name']

class ZDTFDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset =ZDTF.objects.all()
    serializer_class = ZDTFSerializer
    
class DFPList(generics.ListCreateAPIView):
    queryset= DFP.objects.all()
    serializer_class =DFPSerializer
    filter_backends =[DjangoFilterBackend]
    filterset_fields =['name']

class DFPDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset =DFP.objects.all()
    serializer_class = DFPSerializer
    
class RegionList(generics.ListCreateAPIView):
    queryset = Region.objects.all()
    serializer_class = RegionSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['name']

class RegionDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset =Region.objects.all()
    serializer_class = RegionSerializer
    
    
class ProvinceList(generics.ListCreateAPIView):
    queryset = Province.objects.all()
    serializer_class = ProvinceSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['name']

class ProvinceDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset=Province.objects.all()
    serializer_class=ProvinceSerializer
    
class CommuneList(generics.ListCreateAPIView):
    queryset = Commune.objects.all()
    serializer_class = CommuneSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['name']

class CommuneDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset=Commune.objects.all()
    serializer_class= CommuneSerializer
    
class ForestList(generics.ListCreateAPIView):  
    queryset = Forest.objects.all()
    serializer_class = ForestSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['forest_name']

class ForestDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset=Forest.objects.all()
    serializer_class=ForestSerializer
        
class CantonList(generics.ListCreateAPIView): 
    queryset = Canton.objects.all()
    serializer_class = CantonSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['canton_name']

class CantonDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset =Canton.objects.all()
    serializer_class = CantonSerializer
    
class GroupeList(generics.ListCreateAPIView): 
    queryset = Groupe.objects.all()
    serializer_class = GroupeSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['groupe_name']
    
class GroupeDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset= Groupe.objects.all()
    serializer_class= GroupeSerializer

class ParcelleList(generics.ListCreateAPIView): 
    queryset = Parcelle.objects.all()
    serializer_class = ParcelleSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['parcelle_name']
    
class ParcelleDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset= Parcelle.objects.all()
    serializer_class = ParcelleSerializer
    
class SpeciesList(generics.ListCreateAPIView): 
    queryset = Species.objects.all()
    serializer_class = SpeciesSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['scientific_name']

class SpeciesDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset=Species.objects.all()
    serializer_class= SpeciesSerializer
    
class ParcelSpeciesList(generics.ListCreateAPIView): 
    queryset = ParcelSpecies.objects.all()
    serializer_class = ParcelSpeciesSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['scientific_name']

class ParcelSpeciesDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset=ParcelSpecies.objects.all()
    serializer_class=ParcelSpeciesSerializer
    
@api_view(['GET'])
def get_metadata(request,object_id):
    try:
        metadata=PointCloudMetaData.objects.get(object_id= object_id)
        serializer = PointCloudMetaDataSerializer(metadata)
        return Response(serializer.data)

    except PointCloudMetaData.DoesNotExist:
        return Response({"error": "Metadata not found"},status.HTTP_404_NOT_FOUND)
    
class CesiumIonAssetView(APIView):
    permission_classes = [IsAuthenticated]  # Restrict access as needed

    def get(self, request):
        # Replace with your asset ID and token from Cesium Ion
        asset_data = {
            "asset_id": 2752122,  # Replace with your actual asset ID
            
            "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJqdGkiOiI3OWE3ZmFhOS01M2MzLTRiMWUtODI0ZS05YmJjZjI0ZGYzZDEiLCJpZCI6MjQxNTkyLCJpYXQiOjE3MjYzMDg1Nzl9.p3LFJJ7_1ZYfrf7MgCswSWiJONwnxhBjiO8TymV4NOs", 
        }
        return Response(asset_data)
    
    

# Create your views here.
def cesium_view(request):
    return render(request, 'index.html')

def home(request):
    return render(request, 'home.html')


