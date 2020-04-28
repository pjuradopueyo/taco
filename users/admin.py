from django.contrib import admin
from django.contrib.gis.admin import OSMGeoAdmin

# Register your models here.
from .models import Petition, ResponsePetition, Tag, Category, Provider, Product, Place

admin.site.register(Petition)
admin.site.register(ResponsePetition)
admin.site.register(Tag)
admin.site.register(Category)
admin.site.register(Provider)
admin.site.register(Product)

@admin.register(Place)
class PlaceAdmin(admin.ModelAdmin):
    list_display = ('name', 'visibility','location')
