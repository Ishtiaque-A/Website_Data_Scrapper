# scraper/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('submit/', views.submit_link, name='submit_link'),
    path('data/', views.list_scraped_data, name='list_scraped_data'),
]

