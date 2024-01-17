'''
Created on 2023/12/13

@author: t21cs011
'''
from django.urls import path
from .views import CustomLogoutView, LoginView

app_name = 'login'
urlpatterns = [
    path('', LoginView.as_view(), name="login"),
    path('logout/',CustomLogoutView.as_view(), name="logout"),
]