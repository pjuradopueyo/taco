"""taco URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from allauth.account.views import confirm_email
from django.conf.urls import url
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static 
from rest_framework.urlpatterns import format_suffix_patterns
from users import views


urlpatterns = [
    path('', views.index),
    path('home', views.home, name='home'),
    path('users/', include('users.urls')),
    path('api/', include('api.urls')),
    path('provider/<int:provider_id>/', views.provider, name='provider'),
    path('providers/', views.latest_provider_list,name='latest_provider_list'),
    path('petition/<int:petition_id>/', views.petition, name='petition'),
    path('petition/add/<str:petition_type>', views.petition_add, name = 'petition_add'),
    path('petition/detail/<int:pk>', views.petition_add_detail, name = 'petition_add_detail'),
    path('ajax/petition/join/', views.petition_join, name='petition_join'),
    path('ajax/providers/', views.ajax_provider_list,name='ajax_provider_list'),
    path('admin/', admin.site.urls),
    url(r'^rest-auth/', include('rest_auth.urls')),
    url(r'^rest-auth/registration/', include('rest_auth.registration.urls')),
    url(r'^account/', include('allauth.urls')),
    url(r'^accounts-rest/registration/account-confirm-email/(?P<key>.+)/$', confirm_email, name='account_confirm_email'),
    url(r'^accounts/', include('allauth.urls')),
    path('private/petitions/', views.private_petition_list,name='private_petition_list'),
    path('private/petition/<int:pk>', views.private_petition,name='private_petition'),
    path('private/myaccount', views.my_account, name = 'my_account'),
    path('private/places/', views.private_place_list,name='private_place_list'),
    path('private/place/add', views.place_add, name = 'place_add'),
    path('private/place/<int:pk>', views.private_place,name='private_place'),
    path('private/following/', views.private_following_list,name='private_following_list'),
    path('private/user/<int:pk>', views.private_user,name='private_user'),
    path('private/providers/', views.private_provider_list,name='private_provider_list'),
    path('private/provider/<int:pk>', views.private_provider,name='private_provider'),

    path('image_upload', views.provider_image_view, name = 'image_upload'), 
    path('success', views.success, name = 'success'),
    path('base_layout', views.base_layout),
    path('', include('pwa.urls')),

]

urlpatterns = format_suffix_patterns(urlpatterns)

if settings.DEBUG:
        urlpatterns += static(settings.MEDIA_URL,
                              document_root=settings.MEDIA_ROOT)
