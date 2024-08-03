from django.urls import path
from .views import fetch_rss_feed

urlpatterns = [
    path('fetch/', fetch_rss_feed, name='fetch_rss_feed'),
]
