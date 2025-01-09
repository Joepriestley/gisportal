
from django.shortcuts import render
from django.conf import settings 
import requests,logging
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from rest_framework.response import Response 
from rest_framework import generics, status 
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend

from gisportal.models import  (DRANEF,DPANEF,ZDTF,DFP,Region, Province, Commune, Forest, Canton, Groupe, Parcelle,Species,ParcelSpecies,PointCloudMetaData,ShapefileUpload)

from gisportal.serializers import (DRANEFSerializer,DPANEFSerializer,ZDTFSerializer,DFPSerializer,RegionSerializer, ProvinceSerializer, CommuneSerializer, ForestSerializer, CantonSerializer, GroupeSerializer, ParcelleSerializer,SpeciesSerializer,ParcelSpeciesSerializer,PointCloudMetaDataSerializer)

from gisportal.pagination import LargeResultsSetPagination


# Create your views here.
def cesium_view(request):
    return render(request, 'gisportal/index.html')

def home(request):
    return render(request, 'gisportal/home.html')

def portal(request):
    return render(request, 'gisportal/portal.html')

def contact_us(request):
    return render(request, 'gisportal/contact_us.html')

def about_us(request):
    return render(request, 'gisportal/about_us.html')

def signup(request):
    return render(request, 'gisportal/inscription/signup.html')

def login_view(request):
    return render(request, 'authenticate/login.html')








#getting cesium ion token 
class CesiumIonToken(APIView):
    def get(self,request):
        return Response({'access_token': settings.CESIUM_ACCESS_TOKEN})

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
  


@method_decorator(csrf_exempt, name='dispatch')
class CesiumIonAssetView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        access_token = settings.CESIUM_ACCESS_TOKEN
        cesium_api_url = "https://api.cesium.com/v1/assets"

        if not access_token:
            return Response(
                {"error": "Cesium access token is not configured in settings"},
                status=500
            )

        try:
            response = requests.get(
                cesium_api_url,
                headers={"Authorization": f"Bearer {access_token}"},
                timeout=10
            )
            if response.status_code == 200:
                assets = response.json()
                return Response(assets)
            else:
                return Response(
                    {"error": f"Cesium API returned: {response.status_code}"},
                    status=response.status_code
                )
        except requests.RequestException as e:
            return Response(
                {"error": f"An error occurred: {str(e)}"},
                status=500
            )



