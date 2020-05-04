from django import forms 
from .models import *
from PIL import Image
from django.core.files import File
from allauth.account.forms import LoginForm, SignupForm

import json
import logging
import copy
logger = logging.getLogger(__name__)

class CustomUserForm(forms.ModelForm): 
  
    x = forms.FloatField(widget=forms.HiddenInput(),required=False)
    y = forms.FloatField(widget=forms.HiddenInput(),required=False)
    width = forms.FloatField(widget=forms.HiddenInput(),required=False)
    height = forms.FloatField(widget=forms.HiddenInput(),required=False)

    def __init__(self, *args, **kwargs):
        super(CustomUserForm, self).__init__(*args, **kwargs)
        for fieldname, field in self.fields.items():
            field.widget.attrs.update({
                'class': 'form-control'
            })

    class Meta: 
        model = CustomUser 
        fields = ['first_name', 'last_name', 'alias', 'avatar', 'x', 'y', 'width', 'height',] 

    def save(self):
        user = super(CustomUserForm, self).save()
        x = self.cleaned_data.get('x')
        y = self.cleaned_data.get('y')
        w = self.cleaned_data.get('width')
        h = self.cleaned_data.get('height')

        if user.avatar:
            image = Image.open(user.avatar)
            cropped_image = image.crop((x, y, w+x, h+y))
            resized_image = cropped_image.resize((600, 600), Image.ANTIALIAS)
            resized_image.save(user.avatar.path)
        return user



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


class PetitionNewForm(PetitionForm):
    x = forms.FloatField(widget=forms.HiddenInput(),required=False)
    y = forms.FloatField(widget=forms.HiddenInput(),required=False)
    width = forms.FloatField(widget=forms.HiddenInput(),required=False)
    height = forms.FloatField(widget=forms.HiddenInput(),required=False)
    

    def __init__(self, *args, **kwargs):
        super(PetitionNewForm, self).__init__(*args, **kwargs)
        for fieldname, field in self.fields.items():
            field.widget.attrs.update({
                'class': 'form-control'
            })
        self.fields['description'].label = "Add a description (optional)"
        self.fields['petition_img'].label = "Add an image (optional)"

    class Meta:
        model = Petition
        fields = ('title','description','petition_img', 'x', 'y', 'width', 'height', 'petition_type' )
        widgets = {'petition_type': forms.HiddenInput(),
        'answer_to': forms.HiddenInput(),
        'description' : forms.Textarea(attrs={'rows':4})
        }
        exclude = ['user','place','start_date','finish_date','radio','intensity','added_to','provider','privacy','creation_date','product']
    def save(self):
        petition = super(PetitionNewForm, self).save()
        x = self.cleaned_data.get('x')
        y = self.cleaned_data.get('y')
        w = self.cleaned_data.get('width')
        h = self.cleaned_data.get('height')
        if petition.petition_img:
            image = Image.open(petition.petition_img)
            cropped_image = image.crop((x, y, w+x, h+y))
            resized_image = cropped_image.resize((850, 550), Image.ANTIALIAS)
            resized_image.save(petition.petition_img.path)
        return petition


class TacoLoginForm(LoginForm):
    def __init__(self, *args, **kwargs):
        super(TacoLoginForm, self).__init__(*args, **kwargs)
        for fieldname, field in self.fields.items():
            field.widget.attrs.update({
                'class': 'form-control'
            })

class TacoSignupForm(SignupForm):
    def __init__(self, *args, **kwargs):
        super(TacoSignupForm, self).__init__(*args, **kwargs)
        for fieldname, field in self.fields.items():
            field.widget.attrs.update({
                'class': 'form-control'
            })

class PlaceForm(forms.ModelForm): 
  
    x = forms.FloatField(widget=forms.HiddenInput(),required=False)
    y = forms.FloatField(widget=forms.HiddenInput(),required=False)
    width = forms.FloatField(widget=forms.HiddenInput(),required=False)
    height = forms.FloatField(widget=forms.HiddenInput(),required=False)

    class Meta: 
        model = Place 
        fields = ('name','description','place_main_img', 'x', 'y', 'width', 'height', 'location')
        exclude = ['owner']

    def __init__(self, *args, **kwargs):
        super(PlaceForm, self).__init__(*args, **kwargs)
        for fieldname, field in self.fields.items():
            field.widget.attrs.update({
                'class': 'form-control'
            })
        self.fields['description'].label = "Add a description (optional)"
        self.fields['place_main_img'].label = "Add an image (optional)"

    def save(self):
        place = super(Place, self).save()
        x = self.cleaned_data.get('x')
        y = self.cleaned_data.get('y')
        w = self.cleaned_data.get('width')
        h = self.cleaned_data.get('height')
        if place.place_main_img:
            image = Image.open(place.place_main_img)
            cropped_image = image.crop((x, y, w+x, h+y))
            resized_image = cropped_image.resize((850, 550), Image.ANTIALIAS)
            resized_image.save(place.place_main_img.path)
        return place



