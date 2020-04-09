from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, JsonResponse
from django.template import loader
from rest_framework import viewsets
from rest_framework import permissions
from users.serializers import PetitionSerializer, ResponsePetitionSerializer, ProviderSerializer, OfferSerializer, ApplauseSerializer, FollowingSerializer
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Petition, ResponsePetition, Provider, Offer, Applause, Following, CustomUser
from .forms import ProviderForm, PetitionForm, PetitionNewForm, CustomUserForm
from rest_framework import mixins
from rest_framework import generics
# from allauth.socialaccount.providers.facebook.views import FacebookOAuth2Adapter
from allauth.socialaccount.providers.google.views import GoogleOAuth2Adapter
from rest_auth.registration.views import SocialLoginView
from django.core.paginator import Paginator
from django.db.models import Q


import json
import logging
import copy
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

    if request.user.is_authenticated:
        return redirect('private_petition_list') 

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
    count_join = Petition.objects.filter(added_to=petition_id).count()
    count_following = Following.objects.filter(following_to=petition.user.id).count()
    context = {'petition': petition, 'count_join': count_join, 'count_following': count_following}
    return render(request, 'users/petition.html', context)



#######################################################################
# Petition
#######################################################################

#
# Petition - Petition
#
def petition_add(request,petition_type): 
    if request.user.is_authenticated:
        logger.error('Autenticado en el petition add')
    else:
        logger.error('No autenticado')

    if request.method == 'POST': 
 
        if request.user.is_authenticated:
            form = PetitionNewForm(request.POST, request.FILES) 
            if form.is_valid(): 
                result_petition = form.save() 
                result_petition.user=request.user
                result_petition.save()
                return redirect('index') 
        else:
            return redirect('account_login') 

    else:
        answer_to=request.GET.get('petition')
        form = PetitionNewForm(initial={'petition_type': petition_type,'answer_to':answer_to}) 
    return render(request, 'private/petition_add.html', {'form' : form}) 


#
# Petition - Petition
#
def PrivatePetitionList(request): 
    if request.user.is_authenticated:
        logger.error('Autenticado en el petition add')
    else:
        logger.error('No autenticado')

    following_list = Following.objects.filter(user=request.user).values_list('following_to', flat=True).order_by('following_to')
    logger.error('Following ' + str(following_list))
    petition_list = Petition.objects.filter(Q(user__in= following_list) | Q(user=request.user)).order_by('-start_date')
    logger.error('Petition' + str(petition_list))
    context = {'petition_list': petition_list}


    return render(request, 'private/petitions.html', context) 


#######################################################################
# Account
#######################################################################

#
# User - myAccount
#
def my_account(request): 
    if request.user.is_authenticated:
        logger.error('Autenticado en el petition add')
    else:
        logger.error('No autenticado')
    user = get_object_or_404(CustomUser, pk=request.user.id)
    if request.method == 'POST': 
        
        if request.user.is_authenticated:
            form = CustomUserForm(request.POST or None, request.FILES,instance=user) 
            if form.is_valid(): 
                form.save() 
                return redirect('my_account') 
        else:
            return redirect('account_login') 

    else:
        form = CustomUserForm(instance=user) 
    return render(request, 'private/my_account.html', {'form' : form}) 

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

#######################################################################
# Petition
#######################################################################

#
# Petition - Petition
#
def petition_join(request): 
    if request.user.is_authenticated:
        logger.error('Autenticado en el petition add')
    else:
        logger.error('No autenticado')

    if request.method == 'POST': 
        petition_id = request.POST.get('petition_id')
    else:
        return JsonResponse({'status':"invalid method"})

    logger.error('Es un tipo POST con petition_id'+petition_id)
    # Seleccionar si existe ya una con parent tal, y si si, se devuelve un duplicado
    if Petition.objects.filter(added_to=petition_id,user=request.user).count() > 0:
        logger.error('Duplicado')
        return JsonResponse({'status':"duplicated"})
    
    parent = Petition.objects.get(pk=petition_id)
    petition = Petition()
    petition.title = parent.title
    petition.description = parent.description
    petition.place = parent.place
    petition.start_date = parent.start_date
    petition.finish_date = parent.finish_date
    petition.radio = parent.radio
    petition.intensity = parent.intensity
    petition.petition_img = parent.petition_img 
    petition.added_to = parent
    petition.user=request.user
    petition.save()
    return JsonResponse({'id':petition.id})



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
        serializer = FollowingSerializer(data=request.data)
        
        logger.error('Autenticado '+json.dumps(request.data))
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

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