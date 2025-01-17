from django.contrib import admin
from django.urls import path
from django.shortcuts import render
from gisportal.models import (
    DRANEF, DPANEF, DFP, ZDTF, Region, Province, Commune, 
    Forest, Canton, Groupe, Parcelle, Species, ParcelSpecies,EspeceInventaire,Shp
)
from leaflet.admin import LeafletGeoAdmin



# Custom Admin Site
class CustomAdminSite(admin.AdminSite):
    site_header = "Geoportal Globetudes Admin"
    site_title = "Geoportal Admin"

    def get_urls(self):
        # Add custom URLs for the admin dashboard
        urls = super().get_urls()
        custom_urls = [
            path('dashboard/', self.admin_view(self.dashboard_view)),
        ]
        return custom_urls + urls

    def dashboard_view(self, request):
        # Render a custom dashboard page
        stats = {
            'forests': Forest.objects.count(),
            'parcels': Parcelle.objects.count(),
            'species': Species.objects.count(),
        }
        return render(request, 'admin/dashboard.html', {'stats': stats})


# Instantiate the Custom Admin Site
admin_site = CustomAdminSite(name='custom_admin')

# Register models with the custom admin site
admin_site.register(Forest)
admin_site.register(Parcelle)
admin_site.register(Species)


# DRANEF Admin
@admin.register(DRANEF)
class DRANEFAdmin(admin.ModelAdmin):
    list_display = ('id_dranef', 'name')
    search_fields = ('name',)
    list_filter = ('name',)


# DPANEF Admin
@admin.register(DPANEF)
class DPANEFAdmin(admin.ModelAdmin):
    list_display = ('id_dpanef', 'name')
    search_fields = ('name',)
    list_filter = ('name',)


# DFP Admin
@admin.register(DFP)
class DFPAdmin(admin.ModelAdmin):
    list_display = ('id_dfp', 'name')
    search_fields = ('name',)
    list_filter = ('name',)


# ZDTF Admin
@admin.register(ZDTF)
class ZDTFAdmin(admin.ModelAdmin):
    list_display = ('id_zdtf', 'name')
    search_fields = ('name',)
    list_filter = ('name',)


# Region Admin
@admin.register(Region)
class RegionAdmin(LeafletGeoAdmin):
    list_display = ('id_region', 'name')
    search_fields = ('name',)
    list_filter = ('name',)


# Province Admin
@admin.register(Province)
class ProvinceAdmin(LeafletGeoAdmin):
    list_display = ('id_province', 'name')
    search_fields = ('name',)


# Commune Admin
@admin.register(Commune)
class CommuneAdmin(LeafletGeoAdmin):
    list_display = ('id_commune', 'name')
    search_fields = ('name',)
    list_filter = ('name',)



# Forest Admin
@admin.register(Forest)
class ForestAdmin(LeafletGeoAdmin):
    list_display = (
        'id_forest', 'forest_name', 'loca_name', 
        'superficie', 'num_canton', 'num_parcel', 
        'titre_fonci', 'for_formatio'
    )
    search_fields = ('forest_name', 'loca_name')
    list_filter = ('id_forest', 'forest_name')
   



# Canton Admin
@admin.register(Canton)
class CantonAdmin(LeafletGeoAdmin):
    list_display = (
        'id_canton', 'canton_name', 'num_groupe', 
        'superficie', 'forest'
    )
    search_fields = ('canton_name',)
    list_filter = ('id_canton', 'canton_name')
    


# Groupe Admin
@admin.register(Groupe)
class GroupeAdmin(LeafletGeoAdmin):
    list_display = (
        'id_groupe', 'groupe_name', 'superficie', 
        'parcel_num', 'forest', 'canton'
    )
    search_fields = ('groupe_name',)
    list_filter = ('id_groupe', 'groupe_name')
    raw_id_fields = ('forest', 'canton')



# Parcelle Admin
@admin.register(Parcelle)
class ParcelleAdmin(LeafletGeoAdmin):
    list_display = (
        'id_parcel', 'parcelle', 'superficie', 
        'location', 'groupe', 'commune', 'dfp'
    )
    search_fields = ('parcelle',)
    list_filter = ('id_parcel', 'parcelle')


# Species Admin
@admin.register(Species)
class SpeciesAdmin(admin.ModelAdmin):
    list_display = (
        'id_species', 'sci_name', 'vernac_name', 
        'french_name', 'spp_decript'
    )
    search_fields = ('sci_name',)
    list_filter = ('sci_name',)


# ParcelSpecies Admin
@admin.register(ParcelSpecies)
class ParcelSpeciesAdmin(admin.ModelAdmin):
    list_display = ('sci_name', 'num_species', 'parcelle', 'num_total','vol_total')
    search_fields = ('parcelle', 'sci_name')
    list_filter = ('sci_name','parcelle')
    autocomplete_fields = ['sci_name']

# espece_inventaire Admin

@admin.register(EspeceInventaire)
class  EspeceInventaireAdmin(admin.ModelAdmin):
    list_display = ('circonf', 'num_arbre','hauteur', 'vol_arbre','id_parcespp')
    search_fields = ('circonference', 'hauteur')
    list_filter = ('id_parcespp',)
    autocomplete_fields = ['id_parcespp']


@admin.register(Shp)
class ShpAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'model_type', 'date')
    list_filter = ('model_type',)  # Add a filter for model_type
    search_fields = ('name', 'description')