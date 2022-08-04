"""URLs for book."""
from rest_framework import routers
from django.conf.urls import url
from book import views


urlpatterns = [
    url(r'^search_book/',
        views.SearchBookViewSet.as_view()),
    url(r'^review_book/',
        views.ReviewBookViewSet.as_view()),
]
