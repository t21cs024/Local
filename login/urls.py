'''
Created on 2023/12/13

@author: t21cs011
'''
from django.urls import path
<<<<<<< HEAD
from .views import CustomLogoutView, LoginView
=======
from .views import CustomLoginView,  CustomLogoutView, SignUpView
from . import views
>>>>>>> refs/heads/1/17最新master

app_name = 'login'
urlpatterns = [
<<<<<<< HEAD
=======
    #path('',CustomLoginView.as_view()),
>>>>>>> refs/heads/1/17最新master
    path('logout/',CustomLogoutView.as_view(), name="logout"),
<<<<<<< HEAD
    path('', LoginView.as_view(), name="login"),
=======
    path('signup/', SignUpView.as_view(), name="signup"),
    path('', views.LoginView.as_view(), name="login"),
>>>>>>> refs/heads/1/17最新master
]