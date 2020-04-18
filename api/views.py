
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, JsonResponse
from django.template import loader
from django.core.paginator import Paginator, EmptyPage
from django.core import serializers
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.db.models import Count, Case, When, IntegerField
from django.template.loader import render_to_string
from rest_framework import viewsets
from rest_framework import permissions, authentication
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import mixins
from rest_framework import generics
from rest_auth.registration.views import SocialLoginView
# from allauth.socialaccount.providers.facebook.views import FacebookOAuth2Adapter
from allauth.socialaccount.providers.google.views import GoogleOAuth2Adapter
from users.serializers import PetitionSerializer, ResponsePetitionSerializer, ProviderSerializer, OfferSerializer, ApplauseSerializer, FollowingSerializer, FollowingPlaceSerializer, FollowingProviderSerializer
from users.models import Petition, ResponsePetition, Provider, FollowingProvider, Offer, Applause, Following, CustomUser, FollowingPlace, Place, Following
from users.forms import ProviderForm, PetitionForm, PetitionNewForm, CustomUserForm, PlaceForm


import json
import logging
import copy
logger = logging.getLogger(__name__)

# Create your views here.

#######################################################################
# Petition
#######################################################################

#
# Petition - Petition
#
class private_petition_list(APIView):

    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, format=None):
        """
        Return a list of all users.
        """
        page_size = request.GET.get('page_size','10')
        page_number = request.GET.get('page_number','1')

        following_list = Following.objects.filter(
            user=request.user).values_list(
                'following_to', flat=True).order_by('following_to')

        following_list_place = FollowingPlace.objects.filter(
            user=request.user).values_list(
                'place', flat=True).order_by('pk')

        following_list_provider = FollowingProvider.objects.filter(
            user=request.user).values_list(
                'provider', flat=True).order_by('pk')

        petition_full_list = Petition.objects.filter(
            Q(user__in= following_list) | Q(place__in= following_list_place) | Q(provider__in= following_list_provider) | Q(user=request.user)).annotate(
                num_joins=Count('added_to_petition')).annotate(
                    num_offers=Count('answer_to_petition')).annotate(
                        num_applauses=Count('applause')).annotate( i_joined=Count(Case(
                            When(added_to_petition__user__id=request.user.id, then=1),
                            output_field=IntegerField(),
                            ))).annotate( i_clapped=Count(Case(
                            When(applause__user__id=request.user.id, then=1),
                            output_field=IntegerField(),
                            ))).order_by('-start_date')

        paginator = Paginator(petition_full_list, page_size) # Show 25 contacts per page
        if int(page_number) > paginator.num_pages:
            return Response("", status=status.HTTP_204_NO_CONTENT)

        petition_list = paginator.get_page(page_number)
        serializer = PetitionSerializer(petition_list, many=True)
        return Response(serializer.data)


# Social login
class GoogleLogin(SocialLoginView):
    adapter_class = GoogleOAuth2Adapter

""" class FacebookLogin(SocialLoginView):
    adapter_class = FacebookOAuth2Adapter """
    
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
            serializer.save(user=request.user)
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
        petition.num_joins = Petition.objects.filter(added_to_petition=petition).count()
        petition.num_applauses  = Applause.objects.filter(petition=petition).count()
        petition.num_offers  = Petition.objects.filter(answer_to_petition=petition).count()
        petition.i_joined = 0
        petition.i_clapped = 0
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




# API views
# Offer views
class OfferList(APIView):
    """
    List all offers, or create a new petition.
    """
    def get(self, request, format=None):
        offers = Offer.objects.all()
        serializer = OfferSerializer(offers, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = OfferSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class OfferDetail(APIView):
    """
    Retrieve, update or delete a offer instance.
    """
    def get_object(self, pk):
        try:
            return Offer.objects.get(pk=pk)
        except Offer.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        offer = self.get_object(pk)
        serializer = OfferSerializer(offer)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        offer = self.get_object(pk)
        serializer = OfferSerializer(offer, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        offer = self.get_object(pk)
        offer.delete()
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


#
# Contribtions
#
# Provider views
class ProviderList(mixins.ListModelMixin,
                  mixins.CreateModelMixin,
                  generics.GenericAPIView):
    queryset = Provider.objects.all()
    serializer_class = ProviderSerializer

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

class ProviderDetail(mixins.RetrieveModelMixin,
                    mixins.UpdateModelMixin,
                    mixins.DestroyModelMixin,
                    generics.GenericAPIView):
    queryset = Provider.objects.all()
    serializer_class = ProviderSerializer

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)

#
# Contribtions
#
# Applause views
class ApplauseList(mixins.ListModelMixin,
                  mixins.CreateModelMixin,
                  generics.GenericAPIView):
    queryset = Applause.objects.all()
    serializer_class = ApplauseSerializer

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        serializer = ApplauseSerializer(data=request.data)
        
        logger.error('Autenticado '+json.dumps(request.data))
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ApplauseDetail(mixins.RetrieveModelMixin,
                    mixins.UpdateModelMixin,
                    mixins.DestroyModelMixin,
                    generics.GenericAPIView):
    queryset = Applause.objects.all()
    serializer_class = ApplauseSerializer

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)


#
# Contribtions
#
# Applause views
class FollowingList(mixins.ListModelMixin,
                  mixins.CreateModelMixin,
                  generics.GenericAPIView):
    queryset = Following.objects.all()
    serializer_class = FollowingSerializer

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        following = Following.objects.filter(user=request.user,following_to=request.POST.get("following_to"))
        if following:
            following.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            serializer = FollowingSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save(user=request.user)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            else:
                return Response(status=status.HTTP_400_BAD_REQUEST)
                
        


class FollowingDetail(mixins.RetrieveModelMixin,
                    mixins.UpdateModelMixin,
                    mixins.DestroyModelMixin,
                    generics.GenericAPIView):
    queryset = Following.objects.all()
    serializer_class = FollowingSerializer

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)


#
# Contribtions
#
# FollowingPlace views
class FollowingPlaceList(mixins.ListModelMixin,
                  mixins.CreateModelMixin,
                  generics.GenericAPIView):
    queryset = FollowingPlace.objects.all()
    serializer_class = FollowingPlaceSerializer

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        following = FollowingPlace.objects.filter(user=request.user,place=request.POST.get("place"))
        if following:
            following.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            serializer = FollowingPlaceSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save(user=request.user)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class FollowingPlaceDetail(mixins.RetrieveModelMixin,
                    mixins.UpdateModelMixin,
                    mixins.DestroyModelMixin,
                    generics.GenericAPIView):
    queryset = FollowingPlace.objects.all()
    serializer_class = FollowingPlaceSerializer

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)


#
# Contribtions
#
# FollowingPlace views
class FollowingProviderList(mixins.ListModelMixin,
                  mixins.CreateModelMixin,
                  generics.GenericAPIView):
    queryset = FollowingProvider.objects.all()
    serializer_class = FollowingProviderSerializer

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        following = FollowingProvider.objects.filter(user=request.user,provider=request.POST.get("provider"))
        if following:
            following.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            serializer = FollowingProviderSerializer(data=request.data)

            if serializer.is_valid():
                serializer.save(user=request.user)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class FollowingProviderDetail(mixins.RetrieveModelMixin,
                    mixins.UpdateModelMixin,
                    mixins.DestroyModelMixin,
                    generics.GenericAPIView):
    queryset = FollowingProvider.objects.all()
    serializer_class = FollowingProviderSerializer

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)