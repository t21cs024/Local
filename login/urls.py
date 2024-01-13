'''
Created on 2023/12/13

@author: t21cs011
'''
from django.urls import path
from .views import CustomLoginView,  CustomLogoutView

app_name = 'login'
urlpatterns = [
    path('',CustomLoginView.as_view()),
    path('logout/',CustomLogoutView.as_view(), name="logout"),
]