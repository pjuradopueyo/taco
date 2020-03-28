from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from rest_framework import viewsets
from rest_framework import permissions
from users.serializers import PetitionSerializer, ResponsePetitionSerializer
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Petition, ResponsePetition
from rest_framework import mixins
from rest_framework import generics
from allauth.socialaccount.providers.facebook.views import FacebookOAuth2Adapter
from allauth.socialaccount.providers.google.views import GoogleOAuth2Adapter
from rest_auth.registration.views import SocialLoginView

#Web views
def index(request):
    latest_petition_list = Petition.objects.order_by('-start_date')[:5]
    context = {'latest_petition_list': latest_petition_list}
    return render(request, 'users/index.html', context)

# Social login
class GoogleLogin(SocialLoginView):
    adapter_class = GoogleOAuth2Adapter

class FacebookLogin(SocialLoginView):
    adapter_class = FacebookOAuth2Adapter
    
# API views
# Petition views
class PetitionList(APIView):
    """
    List all petitions, or create a new petition.
    """
    def get(self, request, format=None):
        petitions = Petition.objects.all()
        serializer = PetitionSerializer(petitions, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = PetitionSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class PetitionDetail(APIView):
    """
    Retrieve, update or delete a petition instance.
    """
    def get_object(self, pk):
        try:
            return Petition.objects.get(pk=pk)
        except Petition.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        petition = self.get_object(pk)
        serializer = PetitionSerializer(petition)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        petition = self.get_object(pk)
        serializer = PetitionSerializer(petition, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        petition = self.get_object(pk)
        petition.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

#
# Contribtions
#
# Petition views
class ResponsePetitionList(mixins.ListModelMixin,
                  mixins.CreateModelMixin,
                  generics.GenericAPIView):
    queryset = ResponsePetition.objects.all()
    serializer_class = ResponsePetitionSerializer

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

class ResponsePetitionDetail(mixins.RetrieveModelMixin,
                    mixins.UpdateModelMixin,
                    mixins.DestroyModelMixin,
                    generics.GenericAPIView):
    queryset = ResponsePetition.objects.all()
    serializer_class = ResponsePetitionSerializer

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)

