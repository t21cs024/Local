'''
Created on 2023/12/13

@author: t21cs011
'''
from django.urls import path
from .views import CustomLoginView

app_name = 'login'
urlpatterns = [
    path('',CustomLoginView.as_view()),
]