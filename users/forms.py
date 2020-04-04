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

class PetitionForm(forms.ModelForm): 
  
    class Meta: 
        model = Petition 
        fields = "__all__"
    def save(self):
        petition = super(PetitionForm, self).save()
        if petition.petition_img:
            image = Image.open(petition.petition_img)
            cropped_image = image.crop((0, 0, 350, 350))
            resized_image = cropped_image.resize((350, 350), Image.ANTIALIAS)
            resized_image.save(petition.provider_main_img.path)
        return petition

class PetitionNewForm(PetitionForm):
    class Meta:
        model = Petition
        exclude = ['user','place','start_date','finish_date','radio','intensity','added_to']
    def save(self):
        petition = super(PetitionNewForm, self).save()
        return petition
