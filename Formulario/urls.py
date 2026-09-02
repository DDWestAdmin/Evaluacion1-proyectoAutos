from django.urls import path
from . import views

urlpatterns = [
    path('', views.formulario_autos, name='formulario_autos'),
]