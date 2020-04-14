from .models import Petition, ResponsePetition, Provider, Offer, Applause, Following, FollowingPlace, FollowingProvider    
from rest_framework import serializers
from django.db import IntegrityError




class PetitionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Petition
        fields = "__all__"
        read_only_fields = ['user']
    def create(self, validated_data):
        request = Petition.objects.create(**validated_data)
        return request

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
    class Meta:
        model = Provider
        fields = ['id','user','desription','url','provider_main_img','start_date']
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
            request = Following.objects.create(**validated_data)
            return request
        except IntegrityError as e: 
            return "error"


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