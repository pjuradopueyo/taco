from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import ugettext_lazy as _
from datetime import datetime  

from .managers import CustomUserManager


class CustomUser(AbstractUser):
    username = None
    email = models.EmailField(_('email address'), unique=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    spouse_name = models.CharField(blank=True, max_length=100)
    date_of_birth = models.DateField(blank=True, null=True)
    

    def __str__(self):
        return self.email

class Petition(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    title = models.CharField(max_length=500)
    description = models.TextField(null=True, blank=True)
    latitude = models.DecimalField(max_digits=9, decimal_places=6)
    longitude = models.DecimalField(max_digits=9, decimal_places=6)
    start_date = models.DateField()
    finish_date = models.DateField()
    radio = models.IntegerField()
    intensity = models.IntegerField()
    
    class Meta:
        ordering = ['start_date']

class Offer(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    title = models.CharField(max_length=500)
    description = models.TextField(null=True, blank=True)
    latitude = models.DecimalField(max_digits=9, decimal_places=6)
    longitude = models.DecimalField(max_digits=9, decimal_places=6)
    start_date = models.DateField(default=datetime.now, blank=True)
    finish_date = models.DateField()
    radio = models.IntegerField()
    intensity = models.IntegerField()

class Category(models.Model):
    name = models.CharField(max_length=50)
    def __str__(self):
        return self.name

class Tag(models.Model):
    name = models.CharField(max_length=100)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    def __str__(self):
        return self.name +' - '+ self.category.name

class ResponsePetition(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    content = models.CharField(max_length=500)
    petition = models.ForeignKey(Petition, on_delete=models.CASCADE)
    start_date = models.DateField(default=datetime.now, blank=True)

class Provider(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    name = models.CharField(max_length=500)
    description = models.TextField(null=True, blank=True)
    url = models.CharField(max_length=500)
    provider_main_img = models.ImageField(upload_to='images/',null=True, blank=True)
    start_date = models.DateField(default=datetime.now, blank=True)
    def __str__(self):
        return self.name

class TagPetition(models.Model):
    petition = models.ForeignKey(Petition, on_delete=models.CASCADE)
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE)

class TagOffer(models.Model):
    offer = models.ForeignKey(Offer, on_delete=models.CASCADE)
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE)