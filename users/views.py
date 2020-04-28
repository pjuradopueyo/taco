from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, JsonResponse
from django.template import loader
from rest_framework import viewsets
from rest_framework import permissions
from users.serializers import PetitionSerializer, ResponsePetitionSerializer, ProviderSerializer, OfferSerializer, ApplauseSerializer, FollowingSerializer, FollowingPlaceSerializer, FollowingProviderSerializer
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Petition, ResponsePetition, Provider, FollowingProvider, Offer, Applause, Following, CustomUser, FollowingPlace, Place, Following
from .forms import ProviderForm, PetitionForm, PetitionNewForm, CustomUserForm, PlaceForm
from rest_framework import mixins
from rest_framework import generics
# from allauth.socialaccount.providers.facebook.views import FacebookOAuth2Adapter
from allauth.socialaccount.providers.google.views import GoogleOAuth2Adapter
from rest_auth.registration.views import SocialLoginView
from django.core.paginator import Paginator, EmptyPage
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.db.models import Count, Case, When, IntegerField
from django.contrib.gis.geos import fromstr
from django.contrib.gis.geos import Point
from django.contrib.gis.db.models.functions import Distance
from django.template.loader import render_to_string


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
        return redirect('home') 

    latest_petition_list = Petition.objects.order_by('-start_date')[:8]
    latest_provider_list = Provider.objects.order_by('-start_date')[:6]
    latest_offer_list = Offer.objects.order_by('-start_date')[:6]
    context = {'latest_petition_list': latest_petition_list,
    'latest_provider_list': latest_provider_list,
    'latest_offer_list': latest_offer_list}
    return render(request, 'users/index.html', context)

@login_required(redirect_field_name='account_login')
def home(request):

    return render(request, 'private/home.html')

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
@login_required(redirect_field_name='account_login')
def private_petition_list(request):

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
        return HttpResponse('')

    logger.error('Asking for page  ' + page_number + ' of ' + str(paginator.num_pages))
    petition_list = paginator.get_page(page_number)


    context = {'petition_list': petition_list}

    return render(request, 'private/petitions.html', context) 


#
# Petition - Petition
#
@login_required(redirect_field_name='account_login')
def private_petition(request,pk):


    petition = Petition.objects.get(pk=pk)

    petition_joins = Petition.objects.filter(added_to=petition.id).count()
    applauses = Applause.objects.filter(petition=petition.id).count()
    offers = Petition.objects.filter(answer_to=petition.id).count()

    petition_list = Petition.objects.filter(added_to=petition.id)[:10]

    context = {'petition': petition,
    'petition_joins': petition_joins,
    'petition_list': petition_list,
    'applauses': applauses,
    'offers': offers}

    return render(request, 'private/petition.html', context) 





#######################################################################
# Place
#######################################################################

#
# Place - Petition
#
@login_required(redirect_field_name='account_login')
def place_add(request): 
    if request.user.is_authenticated:
        logger.error('Autenticado en el place add')
    else:
        logger.error('No autenticado')

    if request.method == 'POST': 
 
        if request.user.is_authenticated:
            form = PlaceForm(request.POST, request.FILES) 
            if form.is_valid(): 
                logger.error('Place form is valid')
                result_place = form.save() 
                result_place.owner=request.user
                result_place.save()
                return redirect('index') 
        else:
            return redirect('account_login') 

    else:
        form = PlaceForm() 
    return render(request, 'private/place_add.html', {'form' : form}) 

#
# Place - Place
#
@login_required(redirect_field_name='account_login')
def private_place_list(request): 

    following_list = FollowingPlace.objects.filter(
        user=request.user).values_list(
            'place', flat=True).order_by('pk')

    logger.error('Places id ' + str(following_list))
    longitude = -87.42906249999996
    latitude = 35.4606699514953
    user_location = Point(longitude, latitude, srid=4326)

    my_place_list = Place.objects.filter(
        Q(pk__in=following_list) | Q(owner=request.user)).order_by('owner').annotate(i_follow=Count(Case(
                        When(followingplace__user__id=request.user.id, then=1)))).annotate(
                            followers=Count("followingplace")).annotate(
                                distance=Distance('location',user_location)).order_by('distance')

    # providers_ids = my_provider_list.values_list('id', flat=True)
    logger.error('Place mine ' + str(my_place_list))

    full_place_list = Place.objects.exclude(
        Q(pk__in=following_list) | Q(owner=request.user)).order_by('-name').annotate(i_follow=Count(Case(
                        When(followingplace__user__id=request.user.id, then=1))))[:8]

    logger.error('Place full ' + str(full_place_list))

    
    context = {'my_place_list': my_place_list,
        'full_place_list': full_place_list}


    return render(request, 'private/places.html', context) 


#
# User - people list
#
@login_required(redirect_field_name='account_login')
def private_place(request,pk): 
    place = get_object_or_404(Place, pk=pk)
    followers = FollowingPlace.objects.filter(place=place).count()
    i_follow = FollowingPlace.objects.filter(user=request.user, place=place).count()
    context = {'place': place,
                'followers': followers,
                "i_follow": i_follow}
    return render(request, 'private/place.html', context) 


#######################################################################
# People
#######################################################################

#
# User - people detail
#
@login_required(redirect_field_name='account_login')
def private_user(request,pk): 
    user = get_object_or_404(CustomUser, pk=pk)
    following = Following.objects.filter(user=user).count()
    followers = Following.objects.filter(following_to=user).count()
    i_follow = Following.objects.filter(user=request.user, following_to=user).count()
    petitions_original = Petition.objects.filter(user=user, added_to__isnull=True).count()
    petitions_joins = Petition.objects.filter(user=user, added_to__isnull=False).count()
    context = {'person': user,
                'following': following,
                'followers': followers,
                'petitions_original': petitions_original,
                'petitions_joins': petitions_joins,
                "i_follow": i_follow}
    return render(request, 'private/user.html', context) 

#
# User - people list
#
@login_required(redirect_field_name='account_login')
def private_following_list(request): 

    following_list = Following.objects.filter(
        user=request.user).order_by('following_to__first_name')

    following_list_id = Following.objects.filter(
        user=request.user).values_list(
            'following_to', flat=True).order_by('following_to')
   
    random_user_list = CustomUser.objects.exclude(
        Q(pk__in = following_list_id) | Q(pk=request.user.id))


    context = {'following_list': following_list,
        'random_user_list': random_user_list}


    return render(request, 'private/following.html', context) 


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
            form = CustomUserForm(request.POST or None, request.FILES,initial={'first_name': request.user.last_name,
            'first_name': request.user.last_name,
            'alias': request.user.alias}, instance=user) 
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
# Place - Place
#
@login_required(redirect_field_name='account_login')
def private_provider_list(request): 

    following_list = FollowingProvider.objects.filter(
        user=request.user).values_list(
            'provider', flat=True).order_by('pk')

    logger.error('Providers id' + str(following_list))

    my_provider_list = Provider.objects.filter(
        Q(pk__in=following_list) | Q(user=request.user)).order_by('name').annotate(i_follow=Count(Case(
                        When(followingprovider__user__id=request.user.id, then=1)))).annotate(followers=Count("followingprovider"))

    # providers_ids = my_provider_list.values_list('id', flat=True)
    logger.error('Providers full' + str(my_provider_list))

    full_provider_list = Provider.objects.exclude(
        Q(pk__in=following_list) | Q(user=request.user)).order_by('-name').annotate(i_follow=Count(Case(
                        When(followingprovider__user__id=request.user.id, then=1))))[:8]



    context = {'my_provider_list': my_provider_list,
        'full_provider_list': full_provider_list}


    return render(request, 'private/providers.html', context) 

#
# User - people list
#
@login_required(redirect_field_name='account_login')
def private_provider(request,pk): 
    provider = get_object_or_404(Provider, pk=pk)
    followers = FollowingProvider.objects.filter(provider=provider).count()
    i_follow = FollowingProvider.objects.filter(user=request.user, provider=provider).count()
    context = {'provider': provider,
                'followers': followers,
                "i_follow": i_follow}
    return render(request, 'private/provider.html', context) 

#
# List - Ajax 
#
@login_required(redirect_field_name='account_login')
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
@login_required(redirect_field_name='account_login')
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






