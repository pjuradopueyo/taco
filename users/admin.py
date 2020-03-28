from django.contrib import admin

# Register your models here.
from .models import Petition, ResponsePetition, Tag, Category

admin.site.register(Petition)
admin.site.register(ResponsePetition)
admin.site.register(Tag)
admin.site.register(Category)