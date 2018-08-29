from django.urls import path
from . import views

urlpatterns = [
    path('rss_reader/', views.rss_reader, name='rss_reader'),
    ]