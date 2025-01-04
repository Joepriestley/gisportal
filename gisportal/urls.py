from django.urls import path 
from .  import views
from gisportal.views import CesiumIonAssetView, CesiumIonToken


app_name = 'gisportal'

urlpatterns=[
    path('api/cesium-ion-token/',CesiumIonToken.as_view(), name="get-cesium-token"),
    
    path('api/metadata/<int:object_id>/', views.get_metadata, name='get_metadata'),
    
    path('dranef/',views.DRANEFList.as_view(),name="dranef"),
    path('dranef/<int:pk>/',views.DRANEFDetailView.as_view(), name="dranef-details"),
    
    path('dpanef/', views.DPANEFList.as_view(),name="dpanef-list"),
    path('dpanef/<int:pk>/', views.DPANEFDetailView.as_view(),name="dpanef-details"),
    
    path('zdtf/', views.ZDTFList.as_view(),name="zdtf-list"),
    path('zdtf/<int:pk>/', views.ZDTFDetailView.as_view(),name="zdtf-details"),
    
    path('dfp/', views.DFPList.as_view(),name="dfp-list"),
    path('dfp/<int:pk>/', views.DFPDetailView.as_view(),name="dfp-Details"),
    
    path('regions/', views.RegionList.as_view(),name="region-list"),
    path('regions/<int:pk>/', views.RegionDetailView.as_view(),name="region-Details"),
    
    path('province/', views.ProvinceList.as_view(),name="province-list"),
    path('province/<int:pk>/', views.ProvinceDetailView.as_view(),name="province-Details"),
    
    path('commune/', views.CommuneList.as_view(),name="commune-list"),
    path('commune/<int:pk>/', views.CommuneDetailView.as_view(),name="commune-Details"),
    
    path('forest/', views.ForestList.as_view(), name="forest-list"),
    path('forest/<int:pk>/', views.ForestDetailView.as_view(), name="forest-Details"),

    path('canton/', views.CantonList.as_view(), name="canton-list"),
    path('canton/<int:pk>/', views.CantonDetailView.as_view(), name="canton-Details"),
    
    path('groupe/', views.GroupeList.as_view(), name="groupe-list"),
    path('groupe/<int:pk>/', views.GroupeDetailView.as_view(), name="groupe-Details"),
    
    path('parcelle/', views.ParcelleList.as_view(), name="parcelle-list"),
    path('parcelle/<int:pk>/', views.ParcelleDetailView.as_view(), name="parcelle-Details"),
    
    path('species/', views.SpeciesList.as_view(), name="species-list"),
    path('species/<int:pk>/', views.SpeciesDetailView.as_view(), name="species-Details"),
    
    path('parcelspecies/', views.ParcelSpeciesList.as_view(), name="parcelspecies-list"),
    path('parcelspecies/<int:pk>/', views.ParcelSpeciesDetailView.as_view(), name="parcelspecies-Details"),
    
    path('uploadedfile/', views.UploadedFileList.as_view(), name="uploaded-list"),
    path('uploadedfile/<int:pk>/', views.UploadedFileDetailView.as_view(), name="uploadedfile-Details"),
    
    path('gisportal/', views.cesium_view, name='gisportal'),
    
    path('home/', views.home, name='home'),
    path('main-portal/',views.portal, name="portal"),
    path('contact_us/', views.contact_us, name='contact_us'),
    path('about_us/', views.about_us, name='about_us'),
    path('signup/',views.signup, name='signup'),
    path('login/', views.login_view, name='authenticate/login'),
    
    path('cesium-ion/', CesiumIonAssetView.as_view(), name='cesium-ion-asset')
    
]