from .models import Petition, ResponsePetition, Provider, Place, Offer, Applause, Following, FollowingPlace, FollowingProvider    
from rest_framework import serializers
from django.db import IntegrityError

import logging
import json
logger = logging.getLogger(__name__)


class PetitionSerializer(serializers.ModelSerializer):
    num_applauses = serializers.IntegerField(required=False)
    num_joins = serializers.IntegerField(required=False)
    num_offers = serializers.IntegerField(required=False)
    i_joined = serializers.IntegerField(required=False)
    i_clapped = serializers.IntegerField(required=False)
    added_to_petition = serializers.StringRelatedField(required=False, many=True)
    distance = serializers.SerializerMethodField(required=False)

    def get_distance(self, obj):
        try:
            return obj.distance.km
        except:
            return None

    class Meta:
        model = Petition
        fields = "__all__"
        read_only_fields = ['user']
    def create(self, validated_data):
        request = Petition.objects.create(**validated_data)
        return request
    def update(self, instance, validated_data):
        instance.title = validated_data.get('title', instance.title)
        #instance.save()
        return instance
        

class OfferSerializer(serializers.ModelSerializer):
    class Meta:
        model = Offer
        fields = "__all__"
        read_only_fields = ['user']
    def create(self, validated_data):
        request = Offer.objects.create(**validated_data)
        return request

        
class ResponsePetitionSerializer(serializers.ModelSerializer):
    class Meta:
        model = ResponsePetition
        fields = ['id','content','petition','user']
    def create(self, validated_data):
        request = ResponsePetition.objects.create(**validated_data)
        return request

class ProviderSerializer(serializers.ModelSerializer):
    i_follow = serializers.IntegerField()
    followers = serializers.IntegerField()
    
    class Meta:
        model = Provider
        fields = "__all__"
    def create(self, validated_data):
        request = Provider.objects.create(**validated_data)
        return request

class PlaceSerializer(serializers.ModelSerializer):
    i_follow = serializers.IntegerField()
    followers = serializers.IntegerField()
    distance = serializers.DecimalField(max_digits=9, decimal_places=6)
    logger.error('Distance en serializer  '+str(distance))

    class Meta:
        model = Place
        fields = "__all__"
    def create(self, validated_data):
        request = Provider.objects.create(**validated_data)
        return request

class ApplauseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Applause
        fields = "__all__"
        read_only_fields = ['user']
    def create(self, validated_data):
        request = Applause.objects.create(**validated_data)
        return request

class FollowingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Following
        fields = "__all__"
        read_only_fields = ['user']
    def create(self, validated_data):
        try:
            logger.error('creando  ')
            request = Following.objects.create(**validated_data)
            logger.error('creado  ')
            return request
        except IntegrityError as e:
            logger.error('Erroraco')
            raise serializers.ValidationError("duplicated")


class FollowingPlaceSerializer(serializers.ModelSerializer):
    class Meta:
        model = FollowingPlace
        fields = "__all__"
        read_only_fields = ['user']
    def create(self, validated_data):
        request = FollowingPlace.objects.create(**validated_data)
        return request

class FollowingProviderSerializer(serializers.ModelSerializer):
    class Meta:
        model = FollowingProvider
        fields = "__all__"
        read_only_fields = ['user']
    def create(self, validated_data):
        request = FollowingProvider.objects.create(**validated_data)
        return request