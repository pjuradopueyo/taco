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
    avatar = models.ImageField(upload_to='avatar/',null=True, blank=True)
    def __str__(self):
        return self.email

class Country(models.Model):
    name = models.CharField(max_length=50)
    def __str__(self):
        return self.name

class Place(models.Model):
    owner = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    name = models.CharField(max_length=500)
    description = models.TextField(null=True, blank=True)
    latitude = models.DecimalField(max_digits=9, decimal_places=6, null=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, null=True)
    country = models.ForeignKey(Country, on_delete=models.CASCADE, null=True)
    town = models.CharField(max_length=500, null=True)
    street = models.CharField(max_length=500, null=True)
    postal = models.CharField(max_length=500, null=True)
    google_place = models.CharField(max_length=500, null=True)
    street_number = models.IntegerField(null=True)
    floor_number = models.IntegerField(null=True)
    door_name = models.CharField(max_length=16, null=True)
    place_main_img = models.ImageField(upload_to='images/',null=True, blank=True)

class Petition(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True)
    title = models.CharField(max_length=500)
    description = models.TextField(null=True, blank=True)
    place = models.ForeignKey(Place, on_delete=models.CASCADE, null=True)
    start_date = models.DateTimeField(default=datetime.now, blank=True)
    finish_date = models.DateTimeField(null=True)
    radio = models.IntegerField(null=True)
    intensity = models.IntegerField(default=50)
    petition_img = models.ImageField(upload_to='petition/', null=True, blank=True)
    added_to = models.ForeignKey('self', on_delete=models.CASCADE, null=True)
    
    class Meta:
        ordering = ['start_date']

class Offer(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    title = models.CharField(max_length=500)
    description = models.TextField(null=True, blank=True)
    latitude = models.DecimalField(max_digits=9, decimal_places=6)
    longitude = models.DecimalField(max_digits=9, decimal_places=6)
    start_date = models.DateTimeField(default=datetime.now, blank=True)
    finish_date = models.DateTimeField()
    radio = models.IntegerField()
    intensity = models.IntegerField()
    offer_img = models.ImageField(upload_to='offer/',null=True, blank=True)
    added_to = models.ForeignKey('self', on_delete=models.CASCADE, null=True)


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
    start_date = models.DateTimeField(default=datetime.now, blank=True)

class Provider(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    name = models.CharField(max_length=500)
    description = models.TextField(null=True, blank=True)
    url = models.CharField(max_length=500)
    provider_main_img = models.ImageField(upload_to='images/',null=True, blank=True)
    secondary_image_1 = models.ImageField(upload_to='images/',null=True, blank=True)
    secondary_image_2 = models.ImageField(upload_to='images/',null=True, blank=True)
    secondary_image_3 = models.ImageField(upload_to='images/',null=True, blank=True)
    secondary_image_4 = models.ImageField(upload_to='images/',null=True, blank=True)
    start_date = models.DateTimeField(default=datetime.now, blank=True)
    def __str__(self):
        return self.name

class TagPetition(models.Model):
    petition = models.ForeignKey(Petition, on_delete=models.CASCADE)
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE)

class TagOffer(models.Model):
    offer = models.ForeignKey(Offer, on_delete=models.CASCADE)
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE)


class TagProvider(models.Model):
    provider = models.ForeignKey(Provider, on_delete=models.CASCADE)
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE)

class Coupon(models.Model):
    provider = models.ForeignKey(Provider, on_delete=models.CASCADE)
    name = models.CharField(max_length=500)
    description = models.TextField(null=True, blank=True)
    url = models.CharField(max_length=500)
    coupon_main_img = models.ImageField(upload_to='images/',null=True, blank=True)
    price = models.IntegerField()

class Applause(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    petition = models.ForeignKey(Petition, on_delete=models.CASCADE)
    start_date = models.DateTimeField(default=datetime.now)
    duration = models.IntegerField(null=True, blank=True)
    claps = models.IntegerField()
    progress = models.IntegerField(null=True, blank=True)