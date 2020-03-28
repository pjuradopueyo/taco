from .models import Petition, ResponsePetition
from rest_framework import serializers


class PetitionSerializer(serializers.ModelSerializer):

    class Meta:
        model = Petition
        fields = ['id','user','title','description','latitude','longitude','start_date','finish_date','radio','intensity']
    def create(self, validated_data):
        request = Petition.objects.create(**validated_data)
        return request

class ResponsePetitionSerializer(serializers.ModelSerializer):
    class Meta:
        model = ResponsePetition
        fields = ['id','content','petition','user']
    def create(self, validated_data):
        request = ResponsePetition.objects.create(**validated_data)
        return request