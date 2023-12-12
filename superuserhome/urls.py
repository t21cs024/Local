'''
Created on 2023/12/12

@author: t21cs011
'''
from django.urls import path,include
from .views import SuperUserHomeView ,UserEditView

app_name = 'superuserhome'
urlpatterns = [
    path('',SuperUserHomeView.as_view()),
    path('useredit/',UserEditView.as_view(), name='useredit'),
    path('orderedit/',include('orderedit.urls'),name='orderedit'),
       ]
