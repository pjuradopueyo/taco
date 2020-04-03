from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.template import loader
from rest_framework import viewsets
from rest_framework import permissions
from users.serializers import PetitionSerializer, ResponsePetitionSerializer, ProviderSerializer, OfferSerializer, ApplauseSerializer
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Petition, ResponsePetition, Provider, Offer, Applause
from .forms import ProviderForm
from rest_framework import mixins
from rest_framework import generics
# from allauth.socialaccount.providers.facebook.views import FacebookOAuth2Adapter
from allauth.socialaccount.providers.google.views import GoogleOAuth2Adapter
from rest_auth.registration.views import SocialLoginView
from django.core.paginator import Paginator

import json
import logging
logger = logging.getLogger(__name__)
#######################################################################
#
# PWA
#
#######################################################################


def base_layout(request):
	template='users/base.html'
	return render(request,template)

#######################################################################
#
# Web views
#
#######################################################################

#######################################################################
# Home
#######################################################################
def index(request):
    latest_petition_list = Petition.objects.order_by('-start_date')[:8]
    latest_provider_list = Provider.objects.order_by('-start_date')[:6]
    latest_offer_list = Offer.objects.order_by('-start_date')[:6]
    context = {'latest_petition_list': latest_petition_list,
    'latest_provider_list': latest_provider_list,
    'latest_offer_list': latest_offer_list}
    return render(request, 'users/index.html', context)

#######################################################################
# Provider
#######################################################################

#
# Provider - Read Only
#
def provider(request,provider_id):
    provider = get_object_or_404(Provider, pk=provider_id)
    context = {'provider': provider}
    return render(request, 'users/provider.html', context)

#
# List - Read Only
#
def latest_provider_list(request):
    latest_provider_list = Provider.objects.order_by('-name')[:50]
    context = {'latest_provider_list': latest_provider_list}
    return render(request, 'users/provider_list.html', context)


#######################################################################
# Provider
#######################################################################

#
# Provider - Read Only
#
def petition(request,petition_id):
    petition = get_object_or_404(Petition, pk=petition_id)
    context = {'petition': petition}
    return render(request, 'users/petition.html', context)


######################################################################
#
# Ajax web
#
######################################################################

#######################################################################
# Provider
#######################################################################

#
# List - Ajax 
#
def ajax_provider_list(request):
    page_size = request.GET.get('page_size')
    page_number = request.GET.get('page_number')
    provider_full_list = Provider.objects.all().order_by('-name')
    paginator = Paginator(provider_full_list, page_size) # Show 25 contacts per page

    provider_list = paginator.get_page(page_number)
    context = {'provider_list': provider_list}
    return render(request, 'users/ajax_provider_list.html', context)

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

# Create your views here. 
def provider_image_view(request): 
  
    if request.method == 'POST': 
        form = ProviderForm(request.POST, request.FILES) 
  
        if form.is_valid(): 
            form.save() 
            return redirect('success') 
    else: 
        form = ProviderForm() 
    return render(request, 'users/provider_form.html', {'form' : form}) 
  
  
def success(request): 
    return HttpResponse('successfully uploaded') 

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