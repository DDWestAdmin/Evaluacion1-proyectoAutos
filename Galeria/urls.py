from django.urls import path
from . import views

urlpatterns = [
    path('', views.galeria_autos, name='galeria_autos'),
]