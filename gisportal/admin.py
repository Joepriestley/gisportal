from django.contrib import admin # type: ignore
from .models import(DRANEF,DPANEF,ZDTF,Region,Province,Commune,Forest,Canton,Groupe,Parcelle,Species,ParcelSpecies )

# Register your models here.
admin.site.register(DRANEF)
admin.site.register(DPANEF)
admin.site.register(ZDTF)
admin.site.register(Region)
admin.site.register(Province)
admin.site.register(Commune)
admin.site.register(Forest)
admin.site.register(Canton)
admin.site.register(Groupe)
admin.site.register(Parcelle)
admin.site.register(Species)
admin.site.register(ParcelSpecies)
