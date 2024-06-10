from django.template.defaulttags import url
from django.urls import include, path
from rest_framework import routers
from rest_framework.authtoken import views

app_name = 'api'

# router = routers.DefaultRouter()


urlpatterns = [
    path('api-token-auth/', views.obtain_auth_token),
]
