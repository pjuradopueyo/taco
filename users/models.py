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
    alias = models.CharField(blank=True, max_length=100)
    date_of_birth = models.DateField(blank=True, null=True)
    avatar = models.ImageField(upload_to='avatar/',null=True, blank=True)
    def __str__(self):
        return self.email

class Country(models.Model):
    name = models.CharField(max_length=50)
    def __str__(self):
        return self.name

class Product(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField(null=True, blank=True)
    url = models.CharField(max_length=100,null=True, blank=True)
    product_main_img = models.ImageField(upload_to='images/',null=True, blank=True)
    price = models.IntegerField(null=True, blank=True)
    def __str__(self):
        return self.name


class Place(models.Model):
    owner = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True)
    name = models.CharField(max_length=500)
    slug = models.CharField(max_length=500)
    visibility = models.CharField(max_length=25,default="public")
    description = models.TextField(null=True, blank=True)
    latitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    country = models.ForeignKey(Country, on_delete=models.CASCADE, null=True, blank=True)
    town = models.CharField(max_length=500, null=True, blank=True)
    street = models.CharField(max_length=500, null=True, blank=True)
    postal = models.CharField(max_length=500, null=True, blank=True)
    google_place = models.CharField(max_length=500, null=True, blank=True)
    street_number = models.IntegerField(null=True, blank=True)
    floor_number = models.IntegerField(null=True, blank=True)
    door_name = models.CharField(max_length=16, null=True, blank=True)
    place_main_img = models.ImageField(upload_to='images/',null=True, blank=True)
    creation_date = models.DateTimeField(default=datetime.now, blank=True)


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

class Petition(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True, blank=True)
    title = models.CharField(max_length=500)
    description = models.TextField(null=True, blank=True)
    place = models.ForeignKey(Place, on_delete=models.CASCADE, null=True, blank=True)
    creation_date = models.DateTimeField(default=datetime.now, blank=True)
    start_date = models.DateTimeField(default=datetime.now, blank=True)
    finish_date = models.DateTimeField(null=True, blank=True)
    radio = models.IntegerField(null=True, blank=True)
    intensity = models.IntegerField(default=50)
    privacy = models.CharField(max_length=15, default='public')
    petition_img = models.ImageField(upload_to='petition/', null=True, blank=True)
    added_to = models.ForeignKey('self', related_name='added_to_petition', on_delete=models.CASCADE, null=True, blank=True)
    petition_type = models.CharField(max_length=10,default='petition')
    answer_to = models.ForeignKey('self', related_name='answer_to_petition', on_delete=models.CASCADE, null=True, blank=True)
    provider = models.ForeignKey(Provider, on_delete=models.CASCADE, null=True, blank=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, null=True, blank=True)
    class Meta:
        ordering = ['start_date']
    def __str__(self):
        return 'media/%s' % (self.user.avatar) #Merezco ser azotado por esto

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
    product = models.ForeignKey(Product, on_delete=models.CASCADE,null=True, blank=True)
    name = models.CharField(max_length=500)
    description = models.TextField(null=True, blank=True)
    url = models.CharField(max_length=500, null=True, blank=True)
    coupon_main_img = models.ImageField(upload_to='images/',null=True, blank=True)
    price = models.IntegerField()

class Applause(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    petition = models.ForeignKey(Petition, on_delete=models.CASCADE)
    start_date = models.DateTimeField(default=datetime.now)
    duration = models.IntegerField(null=True, blank=True)
    claps = models.IntegerField()
    progress = models.IntegerField(null=True, blank=True)

class ProductItem(models.Model):
    provider = models.ForeignKey(Provider, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    description = models.TextField(null=True, blank=True)
    url = models.CharField(max_length=500)
    item_main_img = models.ImageField(upload_to='images/',null=True, blank=True)
    start_date = models.DateTimeField(default=datetime.now)
    affiliate_code = models.CharField(max_length=100, null=True, blank=True)

class Order(models.Model):
    product_item = models.ForeignKey(Product, on_delete=models.CASCADE)
    petition = models.ForeignKey(Petition, on_delete=models.CASCADE)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    description = models.TextField(null=True, blank=True)
    order_main_img = models.ImageField(upload_to='images/',null=True, blank=True)
    start_date = models.DateTimeField(default=datetime.now)
    url = models.CharField(max_length=500, null=True, blank=True)
    status = models.CharField(max_length=25, default='new')


class OfferReaction(models.Model):
    offer_petition = models.ForeignKey(Petition, on_delete=models.CASCADE)
    status = models.CharField(max_length=25, default='accepted')
    date = models.DateTimeField(default=datetime.now)
    message = models.TextField(null=True, blank=True)

class Following(models.Model):
    user = models.ForeignKey(CustomUser, related_name='me', on_delete=models.CASCADE, null=True)
    following_to = models.ForeignKey(CustomUser, related_name='following_to', on_delete=models.CASCADE, null=True)
    status = models.CharField(max_length=15, default='accepted')
    petition_date = models.DateTimeField(default=datetime.now, blank=True)
    relation_date = models.DateTimeField(null=True, blank=True)
    message = models.TextField(null=True, blank=True)

    class Meta:
        ordering = ['petition_date']
        db_table = 'users_following'
        constraints = [
            models.UniqueConstraint(fields=['user', 'following_to'], name='unique following')
        ]

class FollowingProvider(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True)
    provider = models.ForeignKey(Provider, on_delete=models.CASCADE, null=True)
    status = models.CharField(max_length=15, default='accepted')
    petition_date = models.DateTimeField(default=datetime.now, blank=True)
    relation_date = models.DateTimeField(null=True, blank=True)
    message = models.TextField(null=True, blank=True)

    class Meta:
        ordering = ['petition_date']

class FollowingPlace(models.Model):
    user = models.ForeignKey(CustomUser,  on_delete=models.CASCADE, null=True)
    place = models.ForeignKey(Place, on_delete=models.CASCADE, null=True)
    status = models.CharField(max_length=15, default='accepted')
    petition_date = models.DateTimeField(default=datetime.now, blank=True)
    relation_date = models.DateTimeField(null=True, blank=True)
    message = models.TextField(null=True, blank=True)

    class Meta:
        ordering = ['petition_date']