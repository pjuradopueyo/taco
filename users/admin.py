from django.contrib import admin

# Register your models here.
from .models import Petition, ResponsePetition, Tag, Category, Provider, Product

admin.site.register(Petition)
admin.site.register(ResponsePetition)
admin.site.register(Tag)
admin.site.register(Category)
admin.site.register(Provider)
admin.site.register(Product)