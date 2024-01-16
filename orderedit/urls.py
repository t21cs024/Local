'''
Created on 2023/12/12

@author: t21cs011
'''
from django.urls import path
from .views import OrderEditView ,NewItemView ,OldItemView

app_name = 'orderedit'  # ordereditアプリケーションに名前空間を指定

urlpatterns = [
    path('', OrderEditView.as_view(), name='orderedit'),  # これは管理画面としてのOrderEditViewですか？
    path('newitem/', NewItemView.as_view(), name='newitem'),
    path('olditem/', OldItemView.as_view(), name='olditem'),
]