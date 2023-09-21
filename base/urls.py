from django.contrib import admin
from django.urls import include, path

from base import views

urlpatterns = [
    path('list.html', views.GetPokemonList.as_view(), name='pokemon.list'),
    path('<slug:key>/detail.html', views.GetPokemonDetail.as_view(), name='pokemon.detail'),
]
