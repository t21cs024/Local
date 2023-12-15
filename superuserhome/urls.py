'''
Created on 2023/12/12

@author: t21cs011
'''
from django.urls import path,include
from .views import SuperUserHomeView ,UserEditView, OrderEditView, OldItemView, NewItemView
from .views import UserEditView,UserInformationView,SignUpView,TestView

app_name = 'superuserhome'
urlpatterns = [
    path('',SuperUserHomeView.as_view()),
    path('useredit/',UserEditView.as_view(), name='useredit'),
    path('orderedit/',OrderEditView.as_view(),name='orderedit'),
    path('userinformation/', UserInformationView.as_view(), name='userinformation'),
    path('signup/',SignUpView.as_view(), name='signup'),
    path('test/',TestView.as_view(), name='test'),
    path('orderedit/olditem/', OldItemView.as_view(), name='olditem'),
    path('orderedit/newitem/', NewItemView.as_view(), name='newitem'),
]
