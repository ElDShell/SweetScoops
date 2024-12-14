from django.urls import path
from .views import *
urlpatterns = [
    path('home/', HomeView.as_view(), name='home'),
    path('about/',AboutView.as_view(), name='about'),
    path('contact/',ContactView.as_view(), name='contact'),
    path('service/',ServiceView.as_view(), name='service'),
]
