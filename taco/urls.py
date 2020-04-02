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
from rest_framework_simplejwt import views as jwt_views
from users import views
from rest_framework.urlpatterns import format_suffix_patterns


urlpatterns = [
    path('', views.index),
    path('users/', include('users.urls')),
    path('provider/<int:provider_id>/', views.provider, name='provider'),
    path('providers/', views.latest_provider_list,name='latest_provider_list'),
    path('ajax/providers/', views.ajax_provider_list,name='ajax_provider_list'),
    path('admin/', admin.site.urls),
    url(r'^rest-auth/', include('rest_auth.urls')),
    url(r'^rest-auth/registration/', include('rest_auth.registration.urls')),
    url(r'^account/', include('allauth.urls')),
    url(r'^accounts-rest/registration/account-confirm-email/(?P<key>.+)/$', confirm_email, name='account_confirm_email'),
    path('api/token/', jwt_views.TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', jwt_views.TokenRefreshView.as_view(), name='token_refresh'),
    url(r'^accounts/', include('allauth.urls')),
    path('petitions/', views.PetitionList.as_view()),
    path('petitions/<int:pk>', views.PetitionDetail.as_view()),
    path('offers/', views.PetitionList.as_view()),
    path('offers/<int:pk>', views.PetitionDetail.as_view()),
    path('responses/', views.ResponsePetitionList.as_view()),
    path('responses/<int:pk>', views.ResponsePetitionDetail.as_view()),
    url(r'^rest-auth/facebook/$', views.FacebookLogin.as_view(), name='fb_login'),
    url(r'^rest-auth/google/$', views.GoogleLogin.as_view(), name='gl_login'),
    path('image_upload', views.provider_image_view, name = 'image_upload'), 
    path('success', views.success, name = 'success'),
    path('', include('pwa.urls')),
]

urlpatterns = format_suffix_patterns(urlpatterns)

if settings.DEBUG:
        urlpatterns += static(settings.MEDIA_URL,
                              document_root=settings.MEDIA_ROOT)
