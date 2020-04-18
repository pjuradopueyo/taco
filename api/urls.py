from django.urls import path, include
from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns
from rest_framework_jwt.views import obtain_jwt_token, refresh_jwt_token

from . import views

urlpatterns = [
    path('petitions/', views.PetitionList.as_view()),
    path('petitions/<int:pk>', views.PetitionDetail.as_view()),
    path('petition/list', views.private_petition_list.as_view(), name='api_petition_list'),
    path('offers/', views.PetitionList.as_view()),
    path('offers/<int:pk>', views.PetitionDetail.as_view()),
    path('applauses/', views.ApplauseList.as_view(), name='applauses'),
    path('applauses/<int:pk>', views.ApplauseDetail.as_view()),
    path('following/', views.FollowingList.as_view(), name='following'),
    path('following/<int:pk>', views.FollowingDetail.as_view()),
    path('following_place/', views.FollowingPlaceList.as_view(), name='following_place'),
    path('following_place/<int:pk>', views.FollowingPlaceDetail.as_view()),
    path('following_provider/', views.FollowingProviderList.as_view(), name='following_provider'),
    path('following_provider/<int:pk>', views.FollowingProviderDetail.as_view()),
    path('responses/', views.ResponsePetitionList.as_view()),
    path('responses/<int:pk>', views.ResponsePetitionDetail.as_view()),
    url(r'^rest-auth/google/$', views.GoogleLogin.as_view(), name='gl_login'),
    url(r'^api-token-auth/', obtain_jwt_token),
    url(r'^api-token-refresh/', refresh_jwt_token),
]
