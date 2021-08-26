from django.urls import path
from src.views import *

urlpatterns = [
    path('',home,name='home1'),
    path('success',success,name='success'),
]