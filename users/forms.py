from django import forms 
from .models import *
from PIL import Image
from django.core.files import File

class ProviderForm(forms.ModelForm): 
  
    class Meta: 
        model = Provider 
        fields = ['user', 'name', 'description', 'url','provider_main_img'] 
    def save(self):
        provider = super(ProviderForm, self).save()
        image = Image.open(provider.provider_main_img)
        cropped_image = image.crop((0, 0, 650, 350))
        resized_image = cropped_image.resize((650, 350), Image.ANTIALIAS)
        resized_image.save(provider.provider_main_img.path)