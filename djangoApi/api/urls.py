from django.template.defaulttags import url
from django.urls import include, path
from rest_framework import routers
from rest_framework import authtoken
from rest_framework.authtoken.views import obtain_auth_token

from . import views

app_name = 'api'

# router = routers.DefaultRouter()


urlpatterns = [
    path('api-token-auth/', obtain_auth_token, name='api_token_auth'),
    path('user/', views.UserListView.as_view(), name='user'),
    path('user/<int:pk>/', views.UserDetailView.as_view(), name='user_detail'),
]
