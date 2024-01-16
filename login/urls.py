'''
Created on 2023/12/13

@author: t21cs011
'''
from django.urls import path
from .views import CustomLoginView,  CustomLogoutView, SignUpView
from . import views

app_name = 'login'
urlpatterns = [
    #path('',CustomLoginView.as_view()),
    path('logout/',CustomLogoutView.as_view(), name="logout"),
    path('signup/', SignUpView.as_view(), name="signup"),
    path('', views.LoginView.as_view(), name="login"),
]