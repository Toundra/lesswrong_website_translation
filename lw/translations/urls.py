from django.urls import path
from . import views

urlpatterns = [
    path('search/node', views.search, name='search'),
]
